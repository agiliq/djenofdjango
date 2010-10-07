Chapter 7. Building a Project management application
-------------------------------------------------------
(Topics introduced: File uploads, Integrating with Amazon S3, Complex RSS feeds-builds on chapter 4, Generating graphics using PIL. Sending Email with Django. Generating PDFs for pages. Exporting Data.)

(This and the next chapter would have larger amount of code than the previous chapters. These chapters would be a rehash of previous chapters, and would show how all these concepts work together.)

Diving in. [Code listing]

File uploads. (We allows users to upload files in this app.)
  Using the Django file widget to upload files.
  The problem with large files.
  Using S3, as a file store.
  Restricting access to S3 files, using Django authentication.
  
Advanced RSS feeds.
  Generating RSS feeds per project.
  Password protecting RSS feeds.
  
Using PIL. (We generate charts for the project, so we use PIL)
  Using PIL to generate charts for the project.
  
Sending email.
  The logs for the project are sent to the user via mail. 
  
Genrating PDFs.
  The reports for the project are available as PDF. This is done using HTML2PDF library. 

Exporting PDF.
  The data for a project is accessible in CSV format. Here we show exporting of a data on a per project, or a more granular level.
  

