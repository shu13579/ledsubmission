param([string]$Python = 'python')
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
function Assert-Exit { if ($LASTEXITCODE -ne 0) { throw "Command failed (exit $LASTEXITCODE)" } }
& $Python generate.py --export-rgb
Assert-Exit
$upstream = Join-Path $PSScriptRoot 'work/jixoo'
if (-not (Test-Path -LiteralPath "$upstream/.git")) {
    git clone https://github.com/glaforge/jixoo.git $upstream
    Assert-Exit
}
git -C $upstream checkout 2703d703d7db530a74555b403f3a4a39f6383b55
Assert-Exit
# Only the upstream image codec is needed. These unchanged classes run on Java 17+.
# Building the complete Pixoo network client/CLI still requires Java 21+.
$pngj = Join-Path $PSScriptRoot 'work/lib/pngj-2.1.0.jar'
if (-not (Test-Path -LiteralPath $pngj)) {
    mvn -q org.apache.maven.plugins:maven-dependency-plugin:3.8.1:copy '-Dartifact=ar.com.hjg:pngj:2.1.0' "-DoutputDirectory=$PSScriptRoot/work/lib"
    Assert-Exit
}
$core = Join-Path $upstream 'src/main/java/io/github/glaforge/jixoo'
$sources = @('api/exception/PixooException.java', 'model/PixooFrame.java',
    'model/PixooAnimation.java', 'model/RawRgbBuffer.java', 'image/PixooImage.java',
    'image/ImageProcessor.java', 'image/GifEncoder.java', 'image/GifDecoder.java',
    'image/PngDecoder.java', 'image/BmpDecoder.java') | ForEach-Object { Join-Path $core $_ }
New-Item -ItemType Directory -Force 'work/classes' | Out-Null
javac -cp $pngj -d work/classes @sources JixooExport.java
Assert-Exit
java -cp "work/classes;$pngj" JixooExport work/rgb submissions
Assert-Exit
& $Python verify.py
Assert-Exit
