I want to create a deep dive analysis of SWE-bench_Pro public dataset. What I want is a static html file that
  allow everyone to deep dive to every single data point of SWE-bench Pro, focusing on the problem statement,
  requirements and interface. At the high level, the data of swe-bench pro is quite large, so likely we need to
  separate the implementation into the HTML file that render the view, and js files contain the logic and the
  actual swe bench pro data.

  THe swe bench pro data can be fetched through hugging face api (see
  @analyze_swe_bench.py). For the ease of future processing, feel free to load all the swe bench pro and store them
   as a single data file in this repo
