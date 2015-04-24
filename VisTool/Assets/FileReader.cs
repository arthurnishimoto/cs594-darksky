using UnityEngine;
using System.Collections;
using System.IO;
using System.Text;

public class FileReader : MonoBehaviour {

	public GameObject pointPrefab;

	public float currentTimeIndex = 0;
	public int maxTimeIndex = 0;

	public bool play = false;
	public float playSpeed = 1;

	// Use this for initialization
	void Start () {
		string[] filenames = ReadDirectory ("../position_results/");

		foreach(string filename in filenames )
		{
			//Debug.Log (filename);
			ReadFile(filename);
		}
	}

	string [] ReadDirectory(string directory) {
		return Directory.GetFiles(directory);
	}

	void ReadFile(string filename) {
		// Open the stream and read it back.
		// Root directory is project folder
		string[] lines = File.ReadAllLines (filename);

		GameObject g = Instantiate (pointPrefab) as GameObject;
		g.transform.parent = transform;
		HaloPoint halo = g.AddComponent<HaloPoint>();
		maxTimeIndex = 0;

		if( filename.LastIndexOf("_") > 0 )
		{
			string id = filename.Substring(filename.LastIndexOf("_")+1, filename.Length-filename.LastIndexOf("_")-1);
			g.name = "halo_"+id;
		}
		foreach( string line in lines)
		{
			string[] positions = line.Split(' ');
			halo.AddPosition(new Vector3(float.Parse(positions[0]),float.Parse(positions[1]),float.Parse(positions[2])));
			maxTimeIndex++;
		}
	}

	public GUIText timeText;

	void Update()
	{
		if( play )
		{
			currentTimeIndex += Time.deltaTime * playSpeed;
			if( currentTimeIndex >= maxTimeIndex )
				currentTimeIndex = 0;
			timeText.text = "Timestamp: " + currentTimeIndex;
		}
	}
}
