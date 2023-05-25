clear
sleep 4
cd /home/avelis
rm -rf ./vilicus
sleep 4
cd /mnt/data/Media
rm -rf ./Movies_temp/
mkdir Movies_temp
sleep 4
mkdir '/mnt/data/Media/Movies_temp/Monsters_University_(2013)'
ffmpeg -ss 5 -i '/mnt/data/Media/Movies/Monsters_University_(2013)/Monsters_University_(2013).mp4' -t 30 -map 0 -c copy '/mnt/data/Media/Movies_temp/Monsters_University_(2013)/Monsters_University_(2013).mp4'
sleep 4
mkdir '/mnt/data/Media/Movies_temp/Superman_II_(1980)/'
ffmpeg -ss 5 -i '/mnt/data/Media/Movies/Superman_II_(1980)/Superman_II_(1980).mkv' -t 30 -map 0 -c copy '/mnt/data/Media/Movies_temp/Superman_II_(1980)/Superman_II_(1980).mkv'
sleep 4
mkdir '/mnt/data/Media/Movies_temp/Explorers_(1985)/'
ffmpeg -ss 5 -i '/mnt/data/Media/Movies/Explorers_(1985)/Explorers_(1985).avi' -t 30 -map 0 -c copy '/mnt/data/Media/Movies_temp/Explorers_(1985)/Explorers_(1985).avi'
sleep 4
mkdir '/mnt/data/Media/Movies_temp/The_Amazing_Spider-Man_(2012)/'
ffmpeg -ss 5 -i '/mnt/data/Media/Movies/The_Amazing_Spider-Man_(2012)/The_Amazing_Spider-Man_(2012).mp4' -t 30 -map 0 -c copy '/mnt/data/Media/Movies_temp/The_Amazing_Spider-Man_(2012)/The_Amazing_Spider-Man_(2012).mp4'
sleep 4
mkdir '/mnt/data/Media/Movies_temp/The_Santa_Clause_3_-_The_Escape_Clause_(2006)/'
ffmpeg -ss 5 -i '/mnt/data/Media/Movies/The_Santa_Clause_3_-_The_Escape_Clause_(2006)/The_Santa_Clause_3_-_The_Escape_Clause_(2006).mp4' -t 30 -map 0 -c copy '/mnt/data/Media/Movies_temp/The_Santa_Clause_3_-_The_Escape_Clause_(2006)/The_Santa_Clause_3_-_The_Escape_Clause_(2006).mp4'
sleep 4
mkdir '/mnt/data/Media/Movies_temp/Sin_City_(2005)/'
ffmpeg -ss 5 -i '/mnt/data/Media/Movies/Sin_City_(2005)/Sin_City_(2005).mp4' -t 30 -map 0 -c copy '/mnt/data/Media/Movies_temp/Sin_City_(2005)/Sin_City_(2005).mp4'
sleep 4
mkdir '/mnt/data/Media/Movies_temp/James_And_The_Giant_Peach_(1996)/'
ffmpeg -ss 5 -i '/mnt/data/Media/Movies/James_And_The_Giant_Peach_(1996)/James_And_The_Giant_Peach_(1996).avi' -t 30 -map 0 -c copy '/mnt/data/Media/Movies_temp/James_And_The_Giant_Peach_(1996)/James_And_The_Giant_Peach_(1996).avi'
