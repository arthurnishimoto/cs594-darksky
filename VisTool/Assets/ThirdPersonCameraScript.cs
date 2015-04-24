using UnityEngine;
using System.Collections;

public class ThirdPersonCameraScript : MonoBehaviour {
	public Transform cameraController;
	
	public float cameraYaw = Mathf.PI/2.0f;
	public float cameraPitch = 0;
	
	public float cameraDistance = -2;
	public float verticalOffset = 0.5f; // camera height
	
	public float sensitivityX = -0.1f;
	public float sensitivityY = 0.1f;
	public float zoomSensitivity = 1.0f;
	
	public bool aimMode = false;
	public bool enableRotation = true;
	
	GameObject focusObject;
	public float focusInterpolationTime = 1.0f;
	public float focusInterpolationTimer = 0.0f;
	public Transform newFocusObject;
	public Transform lastFocusObject;
	
	// Use this for initialization
	void Start () {
		if( !cameraController )
			cameraController = Camera.main.transform;
		
		cameraController.transform.rotation = Quaternion.identity;
		focusObject = new GameObject("Camera Focus");
		
		lastFocusObject = transform;
		if( newFocusObject == null )
		{
			newFocusObject = transform;
		}
		
		focusObject.transform.parent = newFocusObject;
		focusObject.transform.position = newFocusObject.position;
	}
	
	// Update is called once per frame
	void Update () {
		if( newFocusObject != lastFocusObject && focusInterpolationTimer < 1 ){
			focusObject.transform.position = Vector3.Lerp( lastFocusObject.position, newFocusObject.position, focusInterpolationTimer );
			focusInterpolationTimer += Time.deltaTime * focusInterpolationTime;
		} else if( newFocusObject != lastFocusObject && focusInterpolationTimer >= 1 ){
			lastFocusObject = newFocusObject;
			focusObject.transform.parent = newFocusObject;
			focusInterpolationTimer = 0;
		} else {
			focusObject.transform.position = newFocusObject.position;
		}
		
		if( Input.GetKeyDown( KeyCode.LeftAlt ) )
			enableRotation = !enableRotation;
		
		// Rotate the camera based on input
		if( enableRotation ){
			cameraYaw += Input.GetAxis("Mouse X") * sensitivityX;
			cameraPitch += Input.GetAxis("Mouse Y") * sensitivityY;
		}
		if( cameraDistance + Input.GetAxis("Mouse ScrollWheel") * zoomSensitivity < 0 )
			cameraDistance += Input.GetAxis("Mouse ScrollWheel") * zoomSensitivity;
		
		// Clamp rotation
		if( cameraYaw > 2 * Mathf.PI )
			cameraYaw -= 2 * Mathf.PI;
		if( cameraYaw < 0 )
			cameraYaw += 2 * Mathf.PI;
		
		if( cameraPitch > Mathf.PI / 2.5f )
			cameraPitch = Mathf.PI / 2.5f;	
		if( cameraPitch < -Mathf.PI / 2.5f )
			cameraPitch = -Mathf.PI / 2.5f;
		
		
		//float horzRadius = cameraDistance * Mathf.Cos(cameraPitch);
		//float y = cameraDistance * Mathf.Sin(cameraPitch);
		//float x = horzRadius * Mathf.Cos(cameraYaw);
		//float z = horzRadius * Mathf.Sin(cameraYaw);
		//camera.transform.position = focusObject.transform.position + new Vector3( x, y + verticalOffset, z );
				
		// Look at the character
		//camera.transform.LookAt( focusObject.transform.position + new Vector3( 0, verticalOffset, 0 ) );
	}
	
	void LateUpdate(){
		// Spherical to cartesian coordinate conversion
		float x = cameraDistance * Mathf.Cos(cameraYaw) * Mathf.Cos(cameraPitch);
		float z = cameraDistance * Mathf.Sin(cameraYaw) * Mathf.Cos(cameraPitch);
		float y = cameraDistance * Mathf.Sin(cameraPitch);
		
		cameraController.transform.position = focusObject.transform.position + new Vector3( x, y + verticalOffset, z );
				
		// Look at the character
		cameraController.transform.LookAt( focusObject.transform.position + new Vector3( 0, verticalOffset, 0 ) );
	}
	
	public void SetFocusObject( Transform newObject ){
		if( focusInterpolationTimer == 0 ){
			newFocusObject = newObject;
		}
	}
}
