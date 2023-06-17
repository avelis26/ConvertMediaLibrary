clear

#echo "Removing vilicus..."
#cd /home/avelis
#rm -rf ./vilicus
#sleep 0.2

echo "Removing Movies_temp..."
cd /mnt/data/Media
rm -rf ./Movies_temp/
sleep 0.2

echo "Making Movies_temp..."
mkdir Movies_temp
sleep 0.2

echo "Converting Monsters_University_(2013)..."
mkdir '/mnt/data/Media/Movies_temp/Monsters_University_(2013)'
sleep 0.2
ffmpeg -loglevel quiet -ss 5 -i '/mnt/data/Media/Movies/Monsters_University_(2013)/Monsters_University_(2013).mp4' -t 64 -map 0 -c copy '/mnt/data/Media/Movies_temp/Monsters_University_(2013)/Monsters_University_(2013).mp4'

echo "Converting Superman_II_(1980)..."
mkdir '/mnt/data/Media/Movies_temp/Superman_II_(1980)/'
sleep 0.2
ffmpeg -loglevel quiet -ss 5 -i '/mnt/data/Media/Movies/Superman_II_(1980)/Superman_II_(1980).mkv' -t 64 -map 0 -c copy '/mnt/data/Media/Movies_temp/Superman_II_(1980)/Superman_II_(1980).mkv'

echo "Converting Explorers_(1985)..."
mkdir '/mnt/data/Media/Movies_temp/Explorers_(1985)/'
sleep 0.2
ffmpeg -loglevel quiet -ss 5 -i '/mnt/data/Media/Movies/Explorers_(1985)/Explorers_(1985).avi' -t 64 -map 0 -c copy '/mnt/data/Media/Movies_temp/Explorers_(1985)/Explorers_(1985).avi'

echo "Converting The_Amazing_Spider-Man_(2012)..."
mkdir '/mnt/data/Media/Movies_temp/The_Amazing_Spider-Man_(2012)/'
sleep 0.2
ffmpeg -loglevel quiet -ss 5 -i '/mnt/data/Media/Movies/The_Amazing_Spider-Man_(2012)/The_Amazing_Spider-Man_(2012).mp4' -t 64 -map 0 -c copy '/mnt/data/Media/Movies_temp/The_Amazing_Spider-Man_(2012)/The_Amazing_Spider-Man_(2012).mp4'

echo "Converting Joker_(2019)..."
mkdir '/mnt/data/Media/Movies_temp/Joker_(2019)/'
sleep 0.2
ffmpeg -loglevel quiet -ss 5 -i '/mnt/data/Media/Movies/Joker_(2019)/Joker_(2019).mp4' -t 64 -map 0 -c copy '/mnt/data/Media/Movies_temp/Joker_(2019)/Joker_(2019).mp4'

echo "Converting Sin_City_(2005)..."
mkdir '/mnt/data/Media/Movies_temp/Sin_City_(2005)/'
sleep 0.2
ffmpeg -loglevel quiet -ss 5 -i '/mnt/data/Media/Movies/Sin_City_(2005)/Sin_City_(2005).mp4' -t 64 -map 0 -c copy '/mnt/data/Media/Movies_temp/Sin_City_(2005)/Sin_City_(2005).mp4'

echo "Converting James_And_The_Giant_Peach_(1996)..."
mkdir '/mnt/data/Media/Movies_temp/James_And_The_Giant_Peach_(1996)/'
sleep 0.2
ffmpeg -loglevel quiet -ss 5 -i '/mnt/data/Media/Movies/James_And_The_Giant_Peach_(1996)/James_And_The_Giant_Peach_(1996).avi' -t 64 -map 0 -c copy '/mnt/data/Media/Movies_temp/James_And_The_Giant_Peach_(1996)/James_And_The_Giant_Peach_(1996).avi'

echo "Converting The_Grinch_(2018)..."
mkdir '/mnt/data/Media/Movies_temp/The_Grinch_(2018)/'
sleep 0.2
ffmpeg -loglevel quiet -ss 5 -i '/mnt/data/Media/Movies/The_Grinch_(2018)/The_Grinch_(2018).mp4' -t 64 -map 0 -c copy '/mnt/data/Media/Movies_temp/The_Grinch_(2018)/The_Grinch_(2018).mp4'

echo "Converting Storks_(2016)..."
mkdir '/mnt/data/Media/Movies_temp/Storks_(2016)/'
sleep 0.2
ffmpeg -loglevel quiet -ss 5 -i '/mnt/data/Media/Movies/Storks_(2016)/Storks_(2016).mkv' -t 64 -map 0 -c copy '/mnt/data/Media/Movies_temp/Storks_(2016)/Storks_(2016).mkv'

echo "Converting Constantine_(2005)..."
mkdir '/mnt/data/Media/Movies_temp/Constantine_(2005)/'
sleep 0.2
ffmpeg -loglevel quiet -ss 5 -i '/mnt/data/Media/Movies/Constantine_(2005)/Constantine_(2005).avi' -t 64 -map 0 -c copy '/mnt/data/Media/Movies_temp/Constantine_(2005)/Constantine_(2005).avi'

echo "Converting Moana_(2016)..."
mkdir '/mnt/data/Media/Movies_temp/Moana_(2016)/'
sleep 0.2
ffmpeg -loglevel quiet -ss 5 -i '/mnt/data/Media/Movies/Moana_(2016)/Moana_(2016).mp4' -t 64 -map 0 -c copy '/mnt/data/Media/Movies_temp/Moana_(2016)/Moana_(2016).mp4'

echo "Done"