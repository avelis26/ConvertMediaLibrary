clear

echo "Removing Shows_temp..."
cd /mnt/data/Media
rm -rf ./Shows_temp/
sleep 0.1

echo "Making Shows_temp..."
mkdir Shows_temp
mkdir '/mnt/data/Media/Shows_temp/Battlefield_Friends_(2012)'
mkdir '/mnt/data/Media/Shows_temp/Battlefield_Friends_(2012)/Battlefield_Friends_Season_4'
sleep 0.1

echo "Battlefield_Friends_-_S04E03_-_Kill_Cam.mp4..."
sleep 0.1
ffmpeg -loglevel quiet -ss 5 -i '/mnt/data/Media/Shows/Battlefield_Friends_(2012)/Battlefield_Friends_Season_4/Battlefield_Friends_-_S04E03_-_Kill_Cam.mp4' -t 5 -map 0 -c copy '/mnt/data/Media/Shows_temp/Battlefield_Friends_(2012)/Battlefield_Friends_Season_4/Battlefield_Friends_-_S04E03_-_Kill_Cam.mp4'

echo "Battlefield_Friends_-_S04E04_-_Recon_C4.mp4..."
sleep 0.1
ffmpeg -loglevel quiet -ss 5 -i '/mnt/data/Media/Shows/Battlefield_Friends_(2012)/Battlefield_Friends_Season_4/Battlefield_Friends_-_S04E04_-_Recon_C4.mp4' -t 5 -map 0 -c copy '/mnt/data/Media/Shows_temp/Battlefield_Friends_(2012)/Battlefield_Friends_Season_4/Battlefield_Friends_-_S04E04_-_Recon_C4.mp4'

echo "Battlefield_Friends_-_S04E05_-_Youtube_Gamer.mp4..."
sleep 0.1
ffmpeg -loglevel quiet -ss 5 -i '/mnt/data/Media/Shows/Battlefield_Friends_(2012)/Battlefield_Friends_Season_4/Battlefield_Friends_-_S04E05_-_Youtube_Gamer.mp4' -t 5 -map 0 -c copy '/mnt/data/Media/Shows_temp/Battlefield_Friends_(2012)/Battlefield_Friends_Season_4/Battlefield_Friends_-_S04E05_-_Youtube_Gamer.mp4'

echo "Battlefield_Friends_-_S04E09_-_Commander_Online.mp4..."
sleep 0.1
ffmpeg -loglevel quiet -ss 5 -i '/mnt/data/Media/Shows/Battlefield_Friends_(2012)/Battlefield_Friends_Season_4/Battlefield_Friends_-_S04E09_-_Commander_Online.mp4' -t 5 -map 0 -c copy '/mnt/data/Media/Shows_temp/Battlefield_Friends_(2012)/Battlefield_Friends_Season_4/Battlefield_Friends_-_S04E09_-_Commander_Online.mp4'

echo "Done"