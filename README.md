# Overview

This project was a collaboration between my project team (me and one other person) and an outdoor lighting company. The goal was to connect the feeling of a song to certain color(s) and display the corresponding color(s) on their lighting modules, enhancing the overall user experience.

Note: This is a rough prototype of the system, with less automation than originally envisioned. To be honest, getting the code to work was a major challenge, and I may have been a bit too ambitious.

I took on the role of the programming engineer for this project.

# Equipment and Resources
We were provided with a 'bridge' (a Raspberry Pi with IoT capabilities) that connects to the company's iPhone app, and three of their light modules.

(If you try to run this code, it won't work as expected, since it depends on the proprietary bridge and app.)

We relied heavily on the company's network engineer for coding and API assistance—without him, this wouldn't have been possible, especially since this was my first time working with Python and API calls.
# Original Concept and Obstacles

The original concept was to integrate with the company's Alexa connection, allowing users to play a song via voice command. The system would then automatically fetch the track URI, perform color calculations, and make decisions autonomously.

However, we ran into many obstacles, largely due to my overambitiousness and inexperience. As a result, we had to pivot to a much simpler, 'manual' implementation for the prototype.
# Method

We decided to use Spotify's API and its "get audio features" function. This function analyzes a song when given its track URI (Universal Resource Identifier) and outputs numerous parameters. The three key parameters we focused on were:
*  Energy (intensity/activity): Ranges from 0 to 1.
*  Valence (positivity): Ranges from 0 to 1.
*  Mode (major/minor key): 0 for minor, 1 for major.

We believed these parameters would offer the most straightforward and objective route to mapping songs to color schemes.


