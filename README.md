<h1>Project Overview</h1>
This project focuses on building a cloud-based web tier on Amazon Web Services (AWS) that receives face recognition requests, stores images in Amazon S3, and fetches classification results from Amazon SimpleDB. 

<h2>Key Features</h2>

<h3>Web Tier</h3>
<ul>
<li>Receives HTTP POST requests with uploaded images (keyed as inputFile).</li>
<li>Stores images in an S3 bucket.</li>
<li>Uses a SimpleDB to look up face recognition results (simulated).</li>
<li>Returns the classification result directly in the HTTP response (e.g., test_00:Paul).</li>
</ul>

<h3>AWS Resources</h3>
<ul>
<li>EC2 for running the web server (t2.micro).</li>

<li>S3 for storing uploaded images.</li>

<li>SimpleDB for storing face recognition lookup data.</li>
</ul>
<h3>Performance and Concurrency</h3>
<ul>
<li>The web tier handles multiple requests concurrently.</li>

<li>Designed to achieve quick response times for up to 1000 concurrent requests.</li>
</ul>
<img width="776" alt="Screenshot 2025-03-27 at 11 39 29 PM" src="https://github.com/user-attachments/assets/4454db9b-4880-4c8a-b518-5608737510e1" />



