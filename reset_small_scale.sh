clear

echo "Removing small_scale..."
cd /mnt/data/Media
rm -rf ./small_scale/
sleep 0.1

echo "Making small_scale..."
cp -vr small_scale_backup small_scale
sleep 0.1

echo "Done"