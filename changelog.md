# Change Log

0.1 - 2019/08/17

- Added readme.md, requires building this out.
- Added `debugout()` to print out debug log to file in `/debug/` folder with timestamp.
- Added `webout()` to print web response.text to file in `/out/` folder with timestamp.
- Added change log for tracking of changes to code.
- Added road map for tracking of what I intend to do next.
- Added `scrape()` to use requests command.
- Added `main()` for running program.
- Added `inbound()` and `parse()` for handling which sites to connect to.
- Replaced all instances of `targets` with `sites` as that is more appropriate in this context.
- Added extensive commenting on what functions are intended to do and how they work.
- Added configuration file to list search terms that would be run against sites.
- Added support for reading the configuration file `conf.ini` in `/conf/` folder.
- Added `passfail()` to determine if site meets criteria in configuration file. Match for blocking
would mean that the WAF check is successful (assuming testing for blocking language.)
- Added `passfail()` results to output and removed `webout()` which is now sending the website results 
to the tuples.
- Added `siteinfo()` to remove the output of the website reponse.text to `out` variable within the parse()
function, as it shouldn't be there.
- Added descriptors for each function in the debug log appends.
- Removed web response from `parse()` function. This (web response) was originally in the `parse()`
function but doesn't really belong there. Since `parse()` needs to run before the program can check the sites, 
it breaks the ability to shift where the output shows up in the output log. Since the point of the program is 
to determine pass/fail checks, the first part of the output shouldn't be a bunch of information that doesn't 
deliver the point.
- Added pretty format through `texttable` for the output. This does not work yet. Can be found in the 
`passfail()` function.
- Verified cross compatibility between Windows, Linux, and Mac
- Added example.txt in debug to initialize the folder


#### Style

Version - Date version complete - Description

- Change 1
- Change 2
