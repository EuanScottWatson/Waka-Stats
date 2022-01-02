#Waka-Stats
A little program that will plot the different languages I've coded in and the amount of time I've coded in them based off the Waka-Time export JSON. The list of languages included are:
```
Python, Swift, Cocoa, Kotlin, Haskell, Java, Markdown and "Other"
```
To add a langauge to look for, add it as an environment variable when calling the file, e.g.:
```
python plot.py C C++ C#
```
This would track for C, C++ and C# too. <br>
You can click on the interactive legend to show and hide lines. `Middle-Click` to show all the lines and `Right-Click` to hide them all. <br>
Here is an example of my Year in Code for 2021-2022, i.e. from when I was introduced to Waka-Time in August until the New Year:

<img src="example.png" alt="drawing" width="800"/>

It will also print out the total statistics in the command line, for example:

```
This data ranges from 2021-08-11 to 2022-01-02
You spent 176.28 hours coding equalling 2.3504 hours per day
Of which you spent:
        74.46 hours coding in Python
        39.69 hours coding in Swift
        17.2 hours coding in Cocoa
        12.2 hours coding in Java
        11.43 hours coding in Kotlin
        7.68 hours coding in Other
        6.82 hours coding in Markdown
        5.68 hours coding in Haskell
```

You just need to include your own json file from Wakatime and call it `data.json` :)