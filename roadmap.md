Last update 2019-08-16

##### Roadmap:

- Automatically review website content for whether it is restricted by web application firewall.
    - Develop filter to identify WAF block messaging
    - Apply filter to response.text
    - Determine how output should be presented (Desire website -> pass/fail, maybe as a table?)
    - Modify output to reflect above choice
- Cleanup that crazy large list of global variables

##### Other:

- 

##### Completed:

- [Complete] I/O for scraping, web response text out and debug.
- [Complete] Accept .txt, .csv, or .log for list of sites to review from `/in/` folder.
- [Complete] Error handling for inbound.
- [Complete] Debug for available functions.
- [Complete] Handles individual files and runs against all sites listed.