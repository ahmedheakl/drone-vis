from gluoncv import utils
video_path = 'https://raw.githubusercontent.com/dmlc/web-data/master/gluoncv/tracking/Coke.mp4'
im_video = utils.download(video_path)
gt_bbox = [298, 160, 48, 80]