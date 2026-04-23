param(
    [string]$mood = "",
    [string]$note = ""   # accepts ♩ ♪ ♫ ♬ directly
)

# Note char → mood (highest intensity wins if multiple chars passed)
$noteMap = [ordered]@{
    [char]0x266C = 'excited'   # ♬
    [char]0x266B = 'happy'     # ♫
    [char]0x266A = 'curious'   # ♪
    [char]0x2669 = 'calm'      # ♩
}

if ($note) {
    foreach ($char in $noteMap.Keys) {
        if ($note.Contains($char)) { $mood = $noteMap[$char]; break }
    }
}

if (-not $mood) { exit 0 }

$soundsDir = Join-Path $PSScriptRoot "sounds"
$wav = Join-Path $soundsDir "$($mood.ToLower()).wav"

if (-not (Test-Path $wav)) {
    Write-Warning "Sound file not found: $wav"
    exit 1
}

# Play using the OS-native tool — no external dependencies
if ($IsWindows -or $env:OS -eq 'Windows_NT') {
    $player = New-Object System.Media.SoundPlayer($wav)
    $player.PlaySync()
} elseif ($IsMacOS) {
    & afplay $wav
} else {
    # Linux: try common players in order
    foreach ($cmd in @('aplay', 'paplay', 'ffplay')) {
        if (Get-Command $cmd -ErrorAction SilentlyContinue) {
            if ($cmd -eq 'ffplay') {
                & ffplay -nodisp -autoexit -loglevel quiet $wav
            } else {
                & $cmd $wav 2>/dev/null
            }
            break
        }
    }
}
