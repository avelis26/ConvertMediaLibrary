clear

shows_temp="Shows_temp"
echo "Removing $shows_temp..."
cd /mnt/data/Media
rm -rf "./$shows_temp/"
echo "Making $shows_temp..."
mkdir $shows_temp
echo "*********************************************************"

folder_name="Archer_(2009)/Archer_Season_5"
show_name="Archer_-_S05E07_-_Smugglers'_Blues.mp4"
echo "Making $shows_temp/$folder_name..."
mkdir -p "$shows_temp/$folder_name"
echo "Converting $show_name..."
ffmpeg -ss 5 -i "/mnt/data/Media/Shows/$folder_name/$show_name" -t 25 -map 0 -c copy "/mnt/data/Media/$shows_temp/$folder_name/$show_name"
echo "*********************************************************"

folder_name="Dark_Matter_(2015)/Dark_Matter_Season_3"
show_name="Dark_Matter_-_S03E13_-_Nowhere_to_Go.mp4"
echo "Making $shows_temp/$folder_name..."
mkdir -p "$shows_temp/$folder_name"
echo "Converting $show_name..."
ffmpeg -ss 5 -i "/mnt/data/Media/Shows/$folder_name/$show_name" -t 25 -map 0 -c copy "/mnt/data/Media/$shows_temp/$folder_name/$show_name"
echo "*********************************************************"

folder_name="Dark_Matter_(2015)/Dark_Matter_Season_3"
show_name="Dark_Matter_-_S03E06_-_One_Last_Card_to_Play.mp4"
echo "Making $shows_temp/$folder_name..."
mkdir -p "$shows_temp/$folder_name"
echo "Converting $show_name..."
ffmpeg -ss 5 -i "/mnt/data/Media/Shows/$folder_name/$show_name" -t 25 -map 0 -c copy "/mnt/data/Media/$shows_temp/$folder_name/$show_name"
echo "*********************************************************"

folder_name="Dark_Matter_(2015)/Dark_Matter_Season_3"
show_name="Dark_Matter_-_S03E12_-_My_Final_Gift_to_You.mp4"
echo "Making $shows_temp/$folder_name..."
mkdir -p "$shows_temp/$folder_name"
echo "Converting $show_name..."
ffmpeg -ss 5 -i "/mnt/data/Media/Shows/$folder_name/$show_name" -t 25 -map 0 -c copy "/mnt/data/Media/$shows_temp/$folder_name/$show_name"
echo "*********************************************************"

folder_name="Heroes_Reborn_(2015)/Heroes_Reborn_Season_1"
show_name="Heroes_Reborn_-_S01E01_S01E02_-_Brave_New_World_-_Odessa.avi"
echo "Making $shows_temp/$folder_name..."
mkdir -p "$shows_temp/$folder_name"
echo "Converting $show_name..."
ffmpeg -ss 5 -i "/mnt/data/Media/Shows/$folder_name/$show_name" -t 25 -map 0 -c copy "/mnt/data/Media/$shows_temp/$folder_name/$show_name"
echo "*********************************************************"

echo "Done"