import logging
import logging.config
from pymediainfo import MediaInfo
from pprint import pprint
from glob import glob
from TMMPythonPackage import GetLoggerDict, TypeTest

logging.config.dictConfig(GetLoggerDict("DEBUG","./Log.log"))
logging.getLogger("default")

def get_video_metadata(video_file_path: str):
	TypeTest(video_file_path, test_type=str, error_msg=f"video_file_path type is {type(video_file_path)} should be str")
	media_info = MediaInfo.parse(video_file_path)	
	general_video_metadata = dict(media_info.tracks[0].to_data().items())
	processed_video_metadata = {
		"codecs_video": general_video_metadata.get("codecs_video"),
		"complete_name": general_video_metadata.get("complete_name"),
		"audio_codecs": general_video_metadata.get("audio_codecs"),
		"duration": general_video_metadata.get("duration"),
		"file_last_modification_date": general_video_metadata.get("file_last_modification_date"),
		"file_size": general_video_metadata.get("file_size"),
		"unique_id": general_video_metadata.get("unique_id")
	}
	return processed_video_metadata


# # specify the directory path
# dir_path = '/ZFS/Storage/Plex/Movies'

# # use glob to find all txt files in the directory
# # mkv_files = glob(dir_path + '/**/*.mkv', recursive=True)
# avi_files = glob(dir_path + '/**/*.avi', recursive=True)
# m4v_files = glob(dir_path + '/**/*.m4v', recursive=True)
# # mp4_files = glob(dir_path + '/**/*.mp4', recursive=True)


# # print the list of txt files found

# # test=(len(mkv_files), len(avi_files), len(m4v_files), len(mp4_files))

# # print(test)
# # print(sum(test))

# # all_files = [*mkv_files, *avi_files, *m4v_files, *mp4_files]
# # all_files = [*avi_files, *m4v_files]

# # all_file_metadata = [get_video_metadata(item) for item in all_files]

# # pprint(len(all_file_metadata))
# # pprint(all_file_metadata[0])
# # pprint(all_file_metadata[0].get("codecs_video"))

# # test = [item for item in all_file_metadata if item.get("codecs_video").upper() != "HEVC"]

# # pprint(test)
# # pprint(len(test))