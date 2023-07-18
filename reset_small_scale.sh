clear

echo "Removing small_scale..."
cd /mnt/data/Media
rm -rf ./small_scale/
sleep 0.1

echo "Making small_scale..."
mkdir small_scale
sleep 0.1

cp -v "/mnt/data/Media/Movies/Captain_America_-_The_First_Avenger_(2011)/Captain_America_-_The_First_Avenger_(2011).mp4" /mnt/data/Media/small_scale/
cp -v "/mnt/data/Media/Movies/Dragnet_(1987)/Dragnet_(1987).avi" /mnt/data/Media/small_scale/
cp -v "/mnt/data/Media/Movies/Rubikon_(2022)/Rubikon_(2022).mp4" /mnt/data/Media/small_scale/
cp -v "/mnt/data/Media/Movies/Teen_Titans_Go!_vs._Teen_Titans_(2019)/Teen_Titans_Go!_vs._Teen_Titans_(2019).mp4" /mnt/data/Media/small_scale/
cp -v "/mnt/data/Media/Movies/Ender's Game (2013) [1080p]/Ender's.Game.2013.1080p.BluRay.x264.YIFY.mp4" /mnt/data/Media/small_scale/

echo "Done"