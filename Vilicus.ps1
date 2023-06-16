param (
    [Parameter(Mandatory = $true, HelpMessage = "Source directory")]
    [ValidateScript({Test-Path $_ -PathType Container})]
    [string]$Source,

    [Parameter(Mandatory = $true, HelpMessage = "Destination directory")]
    [ValidateScript({Test-Path $_ -PathType Container})]
    [string]$Destination,

    [string]$LogFile = "conversion.log"
)

# Global variables to track conversion progress
$totalSavedSpace = 0
$completedConversions = 0

function Probe-VideoEncoding {
    param (
        [Parameter(Mandatory = $true)]
        [string]$FilePath
    )

    # Execute FFmpeg command to probe video encoding
    $result = & ffmpeg -i $FilePath 2>&1

    # Check if the output contains H.265/HEVC
    return $result.ToLower().Contains("hevc")
}

function Convert-MediaFile {
    param (
        [Parameter(Mandatory = $true)]
        [string]$FilePath,

        [Parameter(Mandatory = $true)]
        [string]$DestinationDir
    )

    # Extract the file name and extension
    $fileName = Split-Path -Leaf $FilePath
    $fileBaseName = [System.IO.Path]::GetFileNameWithoutExtension($fileName)
    $fileExt = [System.IO.Path]::GetExtension($fileName)

    # Create the destination file path with H.265/HEVC encoding
    $destinationFilePath = Join-Path -Path $DestinationDir -ChildPath ("{0}_hevc{1}" -f $fileBaseName, $fileExt)

    # Execute FFmpeg command to convert the media file to H.265/HEVC
    & ffmpeg -i $FilePath -c:v libx265 -crf 28 -c:a copy $destinationFilePath

    # Calculate the saved space by comparing file sizes
    $originalSize = (Get-Item $FilePath).Length
    $convertedSize = (Get-Item $destinationFilePath).Length
    $savedSpace = $originalSize - $convertedSize

    # Update the global variables
    $totalSavedSpace += $savedSpace
    $completedConversions++
}

function Convert-MediaLibrary {
    param (
        [Parameter(Mandatory = $true)]
        [string]$SourceDir,

        [Parameter(Mandatory = $true)]
        [string]$DestinationDir,

        [Parameter(Mandatory = $true)]
        [string]$LogFile
    )

    # Create the destination directory if it doesn't exist
    if (-not (Test-Path -Path $DestinationDir -PathType Container)) {
        New-Item -ItemType Directory -Path $DestinationDir | Out-Null
    }

    # Open the log file in append mode
    $log = [System.IO.File]::AppendAllText($LogFile, "Conversion Progress:`n")

    # Walk through the source directory and convert video files
    Get-ChildItem -Path $SourceDir -Recurse | ForEach-Object {
        if ($_.PSIsContainer -eq $false -and $_.Name -match '\.(mp4|mkv|avi|mov)$') {
            $filePath = $_.FullName
            if (-not (Probe-VideoEncoding -FilePath $filePath)) {
                Convert-MediaFile -FilePath $filePath -DestinationDir $DestinationDir
                $log.WriteLine("Converted: $filePath")
            }
        }
    }

    # Log the total saved space and number of conversions
    $log.WriteLine("Total Saved Space: {0} MB" -f ($totalSavedSpace / (1024 * 1024)))
    $log.WriteLine("Completed Conversions: $completedConversions")

    # Close the log file
    $log.Close()
}

# Convert the media library
Convert-MediaLibrary -SourceDir $Source -DestinationDir $Destination -LogFile $LogFile
