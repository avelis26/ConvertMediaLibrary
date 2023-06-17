# Load parameters from JSON file
$parameters = Get-Content -Raw -Path "parameters.json" | ConvertFrom-Json
$inputPath = $parameters.movies_parent_path
$logParentPath = $parameters.log_parent_path
$opsLog = Join-Path $logParentPath $parameters.log_filename
$moviesManifestPath = Join-Path $logParentPath $parameters.movies_manifest_filename
$exitFile = Join-Path $logParentPath $parameters.exit_filename

# Create working directory if it doesn't exist
if (-not (Test-Path $logParentPath)) {
    New-Item -ItemType Directory -Path $logParentPath | Out-Null
}

# Set up logging to file and console
$loggingLevel = "Debug"
$loggingFormat = "%(asctime)s [%(levelname)s] %(message)s"
$loggingHandlers = @(
    New-Object -TypeName "System.Object" -Property @{
        logtype = "File"
        path = $opsLog
        level = $loggingLevel
        format = $loggingFormat
    }
    New-Object -TypeName "System.Object" -Property @{
        logtype = "Console"
        level = $loggingLevel
        format = $loggingFormat
    }
)
$logging = New-Object -TypeName "System.Object" -Property @{
    handlers = $loggingHandlers
}
$logging.handlers.logtype = "File"
$logging.handlers.path = $opsLog
$logging.handlers.level = $loggingLevel
$logging.handlers.format = $loggingFormat

$logging.info("******************************************************")
$logging.info("EXECUTION START")
$logging.debug("input_path:           $inputPath")
$logging.debug("movies_manifest_path: $moviesManifestPath")
$logging.debug("opsLog:               $opsLog")
$logging.debug("exitFile:             $exitFile")
$logging.info("Creating non-h265 movie manifest...")

# Create non-h265 movie manifest
$movieList = @()
$minFileSize = $parameters.min_file_size
Get-ChildItem -Path $inputPath -File -Recurse | ForEach-Object {
    $fileSize = $_.Length
    if ($fileSize -gt $minFileSize) {
        try {
            $probeOutput = ffmpeg.probe($_.FullName)
            foreach ($stream in $probeOutput.streams) {
                if ($stream.codec_type -eq "video" -and $stream.codec_name -ne "hevc") {
                    $movieList += $_.FullName
                    break
                }
            }
        } catch {
            $logging.error("ERROR06: $($_.FullName)")
            $logging.error($_.Exception)
        }
    }
}

$movieSet = $movieList | Select-Object -Unique
$movieSet | Out-File -FilePath $moviesManifestPath
$logging.info("Total Non-h265 Movies: $($movieSet.Count)")
$logging.info("Non-h265 movie manifest created.")

# Read manifest and convert one movie at a time
$exitFlag = $false
$manifestFile = Get-Content -Path $moviesManifestPath
$conversionCounter = 0
foreach ($line in $manifestFile) {
    $conversionCounter++
    ConvertToH265 $line
    if (Test-Path $exitFile) {
        $logging.info("EXECUTION STOPPED BY USER")
        $logging.info("******************************************************")
        $exitFlag = $true
        break
    }
}

$logging.info("EXECUTION STOP")
$logging.info("******************************************************")

# Define function to convert file to H.265
function ConvertToH265($sourceFilePath) {
    $sourceFilePath = $sourceFilePath.Trim()
    $base = [System.IO.Path]::GetFileNameWithoutExtension($sourceFilePath)
    $outputFile = $base + ".mkv"

    try {
        Rename-Item -Path $sourceFilePath -NewName ($sourceFilePath + ".old")
        ffmpeg.input($sourceFilePath + ".old").output($outputFile, "-c:v libx265 -crf 28 -c:a copy").run()
        Start-Sleep -Seconds 2
        ffmpeg.input($outputFile).output("null", "-f null").run()
        $logging.info("Video validation succeeded.")

        $beforeFileSize = (Get-Item -Path ($sourceFilePath + ".old")).Length
        $afterFileSize = (Get-Item -Path $outputFile).Length
        $totalDifference = $beforeFileSize - $afterFileSize
        $spaceSaved = [decimal]::Divide($totalDifference, 1073741824)
        $spaceSaved = [Math]::Round($spaceSaved, 2)

        $logging.debug("Before Size: $beforeFileSize")
        $logging.debug("After Size:  $afterFileSize")
        $logging.debug("Difference:  $totalDifference")

        Remove-Item -Path ($sourceFilePath + ".old")
    } catch {
        $logging.error("ERROR04: $($_.Exception)")
        $logging.error($_.Exception)
        return
    }

    $logging.info("Conversions complete: $conversionCounter")
    $logging.debug("Total Diff:  $totalDifference")
    $logging.info("Gigabytes saved: $spaceSaved GBs")
}

# Define function to check exit file and stop execution if it exists
function SoftExit($exitFilePath) {
    if (Test-Path $exitFilePath) {
        $logging.info("EXECUTION STOPPED BY USER")
        $logging.info("******************************************************")
        $exitFlag = $true
    }
}

# Start the main script execution
$exitFilePath = Join-Path $logParentPath $exitFile
SoftExit $exitFilePath
$exitFlag = $false
$manifestFile = Get-Content -Path $moviesManifestPath
$conversionCounter = 0
foreach ($line in $manifestFile) {
    $conversionCounter++
    ConvertToH265 $line
    if ($exitFlag) {
        break
    }
    SoftExit $exitFilePath
}
$logging.info("EXECUTION STOP")
$logging.info("******************************************************")
