using UnityEngine;
using System.Collections;

public class HaloPoint : MonoBehaviour {

	public int halo_id = -1;

	public ArrayList positions;

	public int timeIndex = 0;

	// Use this for initialization
	void Start () {
	}

	public void AddPosition( Vector3 newPos )
	{
		if( positions == null )
			positions = new ArrayList();
		positions.Add (newPos);
	}

	// Update is called once per frame
	void Update () {
		if( transform.parent.GetComponent<FileReader>() )
			timeIndex = (int)transform.parent.GetComponent<FileReader>().currentTimeIndex;
		if( timeIndex <= positions.Count - 1 )
			transform.position = (Vector3)positions[timeIndex];
	}
}
