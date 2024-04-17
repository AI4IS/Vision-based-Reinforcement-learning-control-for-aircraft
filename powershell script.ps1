$scriptBlock1 = {
    Set-Location "C:\Users\admin\Desktop\dds_proj\dds_test6"
    .\publisher -DCPSConfigFile config_Pub.ini
}
$scriptBlock2 = {
    Set-Location "C:\Users\admin\Desktop\dds_proj\dds_test6"
    .\subscriber -DCPSConfigFile config_Sub.ini
}

$scriptBlock3 = {
    Set-Location "C:\Users\admin\Desktop\dds_proj\dds_test7"
    .\publisher -DCPSConfigFile config_Pub.ini
}

$scriptBlock4 = {
    Set-Location "C:\Users\admin\Desktop\dds_proj\dds_test7"
    .\subscriber -DCPSConfigFile config_Sub.ini
}

$scriptBlocks = @($scriptBlock1, $scriptBlock2, $scriptBlock3, $scriptBlock4)

Add-Type -TypeDefinition @"
    using System;
    using System.Runtime.InteropServices;

    public class ConsoleWindow {
        [DllImport("kernel32.dll", SetLastError = true)]
        public static extern IntPtr GetConsoleWindow();

        [DllImport("user32.dll", SetLastError = true)]
        public static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint);
    }
"@

Add-Type -AssemblyName PresentationFramework
$screenWidth = [System.Windows.SystemParameters]::PrimaryScreenWidth + 400
$screenHeight = [System.Windows.SystemParameters]::PrimaryScreenHeight + 200

$windowWidth = $screenWidth / 2
$windowHeight = $screenHeight / 2

$positions = @(
    @{ X = 0; Y = 0 },
    @{ X = $windowWidth; Y = 0 },
    @{ X = 0; Y = $windowHeight },
    @{ X = $windowWidth; Y = $windowHeight }
)

$loopIndex = 0

foreach ($position in $positions) {

    $scriptBlock = $scriptBlocks[$loopIndex]
    $process = Start-Process "powershell.exe" -ArgumentList ("-NoExit", "-Command", $scriptBlock) -WindowStyle Normal -PassThru
    Start-Sleep -Milliseconds 100
    $hWnd = $process.MainWindowHandle
    [ConsoleWindow]::MoveWindow($hWnd, [int]$position.X, [int]$position.Y, [int]$windowWidth, [int]$windowHeight, $true)
    $loopIndex++
}
