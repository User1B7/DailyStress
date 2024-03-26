import gdown


url = "https://drive.google.com/drive/folders/1PcyGmelnI6FksZtJ0oJCpfQrTWgwLkhw?usp=drive_link"

gdown.download_folder(url, quiet=False)
