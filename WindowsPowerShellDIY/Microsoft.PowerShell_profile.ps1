clear

$WeatherHome = "D:\Programs\weather.rs\"
$BlogHome = "D:\MyPrograms\MyBlog\"

$dayOfWeek      = (Get-Date).DayOfWeek
$terminalWidth  = $Host.UI.RawUI.WindowSize.Width
$terminalHeight = $Host.UI.RawUI.WindowSize.Height

function Pro { notepad $PROFILE }
function wedit { notepad $WeatherHome/config.ini }
function cc  { clear }

function Prompt {
  $dayOfWeek      = (Get-Date).DayOfWeek
  $terminalWidth  = $Host.UI.RawUI.WindowSize.Width
  $terminalHeight = $Host.UI.RawUI.WindowSize.Height

  $weather = " " + (Get-Content ($WeatherHome + "weather.txt")) + " "
  $temperature = " " + (Get-Content ($WeatherHome + "temperature.txt")) + "°C "

  $curLoc  = " " + (Get-Location) + " "
  $curDate = " " + (Get-Date -Format "HH:mm:ss")     + " "

  Write-Host("$ [")    -NoNewLine
  Write-Host($curLoc)  -NoNewLine -BackgroundColor Yellow -ForegroundColor Black
  Write-Host("|")      -NoNewLine
  Write-Host($curDate) -NoNewLine -BackgroundColor Red -ForegroundColor White
  Write-Host("]")      -NoNewLine

  # 显示星期
  $lineLength = $curLoc.length + $curDate.length + 5
  $diff = $terminalWidth - $lineLength - 9
  if ($diff -ge 0) {

    $weekShort = " " + ("$($dayOfWeek)".SubString(0, 3)) + " "
    Write-Host(" " + ("-" * $diff) + " ") -NoNewLine
    Write-Host("[")        -NoNewLine
    Write-Host($weekShort) -NoNewLine -BackgroundColor DarkCyan -ForegroundColor White
    Write-Host("]")
  }

  # 显示天气
  Write-Host("  [")        -NoNewLine
  Write-Host($weather)     -NoNewLine -BackgroundColor Cyan -ForegroundColor Black
  Write-Host("|")          -NoNewLine
  Write-Host($temperature) -NoNewLine -BackgroundColor Blue -ForegroundColor White
  Write-Host("]")          -NoNewLine

  # 显示 git
  $lineLength = $weather.length + $temperature.length + 5
  git rev-parse | Out-Null
  if($?){
		$gitBranch = " " + "$(git branch --show-current --no-color)" + " "
    $diff = $terminalWidth - $lineLength - $gitBranch.length - 12
    if ($diff -ge 0) {
      Write-Host(" " + ("-" * $diff) + " ") -NoNewLine
      Write-Host("[ ")       -NoNewLine
      Write-Host("Git:")     -NoNewLine -ForegroundColor Red
      Write-Host($gitBranch) -NoNewLine -BackgroundColor DarkRed -ForegroundColor White
      Write-Host(" ]")       -NoNewLine
    }
	}

  return "`n=> "
}
