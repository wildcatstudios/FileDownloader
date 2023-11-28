from tqdm import tqdm
import requests


url = input("import file url for download: ")
file_name = input("import file name: ")
file_name = "newFile" if file_name == '' else file_name
file_name += "."
# Streaming, so we can iterate over the response.
response = requests.get(url, stream=True)
# Content-Type for file type
ct_list = {"application/octet-stream": "apk", "video/x-msvideo": "avi", "text/css": "css", "application/msword": "doc",
           "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx", "text/html": "html",
           "image/jpeg": "jpeg", "text/javascript": "js", "application/json": "json", "audio/mpeg": "mp3", "video/mp4": "mp4",
           "image/png": "png", "application/pdf": "pdf", "application/vnd.rar": "rar", "text/plain": "txt", "application/vnd.ms-excel": "xls",
           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx", "application/zip": "zip"}
# Complete ct_list for more file content-types
if response.headers["Content-Type"] in ct_list.keys():
    file_name += ct_list[response.headers["Content-Type"]]
else:
    file_name += response.headers["Content-Type"]
total_size_in_bytes = int(response.headers.get('content-length', 0))
block_size = 1024  # 1 Kilobyte
progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
with open(file_name, 'wb') as file:
    for data in response.iter_content(block_size):
        progress_bar.update(len(data))
        file.write(data)
progress_bar.close()
if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
    print("ERROR, something went wrong")

