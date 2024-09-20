<?php
header('Content-Type: application/vnd.apple.mpegurl');

// Directorio local donde se almacenan los M3U8 temporales
$path = "github.com/dca2107/ctv/blob/main/hls/SV-23-TVO.m3u8"; // Ruta local en el servidor (no URL HTTP)
$files = glob($path . "*.m3u8");

echo "#EXTM3U\n";
echo "#EXT-X-VERSION:3\n";

foreach ($files as $file) {
    echo "#EXT-X-STREAM-INF:BANDWIDTH=2800000,RESOLUTION=1920x1080,CODECS=\"avc1.640029,mp4a.40.2\"\n";
    echo "https://conceptoweb-studio.com/radio/video/tvo/" . basename($file) . "\n"; // URL completa correcta
}
?>
