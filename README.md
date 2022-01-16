# Intro
* pysocialforce: https://github.com/yuxiang-gao/PySocialForce


# Concept

# Usage
## Simulation
### settings.json
```json
{
    "path":{
        "vid_folder_path": "folder_path",
        "result_folder_path": "folder_path"
    },
    "parameters":{
        
    }
}
```

### do
```bash
python app_simulate.py [idx] [force_idx]
```

## Validation
```bash
python app_validate.py [idx] [force_idx]
```


# workspace
## video folder
### folder name
* video_index
### folder
* [video_index].csv
* hp.csv
* vp.csv
### d

## result folder
### folder name
* video_index + force_index

### files
* initial_data
    * data.json
    * gt.json
* result
    * animate.gif
    * plot.png
    * result.json
* valid
    * valid.json