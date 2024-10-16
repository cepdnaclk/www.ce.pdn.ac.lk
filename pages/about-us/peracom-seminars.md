---
layout: page
title: Peracom Seminars
permalink: /peracom-seminars/
navbar_active: About Us
---

# Peracom Seminars

<div class="text-justify">
  <p>
    Peracom Seminars is a series of seminars hosted by the Department of Computer Engineering, University of Peradeniya, since May 2021. These seminars aim to inspire undergraduates and promote collaborative research by connecting students with leading industry professionals, academics, and researchers from around the world. With a focus on cutting-edge research and technological innovations in computer engineering and related fields, the series has successfully fostered engaging discussions and knowledge sharing among participants.
  </p>

  <p>
    Each seminar lasts approximately 1-1.5 hours, with 40 minutes dedicated to the speaker's presentation followed by a 20-minute interactive Q&A session. Our audience primarily consists of undergraduate and postgraduate students in fields such as Computer Engineering, Computer Science, and Electrical and Electronics Engineering, along with academic staff members. 
  </p>

  <p>
    Peracom Seminars are typically conducted online via Zoom™ to facilitate participation from international guest speakers. However, we also encourage physical seminars whenever possible, as they offer a more interactive experience between the speakers and the audience. 
  </p>
</div>

---

### Join Our Next Seminar

<div class="card">
  <div class="card-body">
    <h5 class="card-title">Seminar Name</h5>
    <p class="card-text"><strong>Date:</strong> </p> <!--  Month Date, 2024-->
    <p class="card-text"><strong>Speaker:</strong> </p> <!--  Dr. _ (University of _ )-->
    
    <div class="d-flex align-items-center mt-3">
      <img src="https://upload.wikimedia.org/wikipedia/commons/7/7b/Zoom_Communications_Logo.svg" alt="Zoom Logo" class="me-2" style="width: 20px;">
      <a href="https://bit.ly/PeraComSeminars" target="_blank" class="btn btn-primary btn-sm">Join via Zoom</a>
    </div>
  </div>
</div>
---
### Gallery

Posters from our previous seminars in 2024:
<div class="d-flex justify-content-center">
<!-- Seminar Posters Carousel -->
<div id="peracomSeminarCarousel2024" class="carousel slide w-50" data-bs-ride="carousel">
  <div class="carousel-inner">
    {% for slide in site.data.peracom_seminars.carousel2024 %}
    <div class="carousel-item{% if forloop.first %} active{% endif %}" data-bs-interval="{{ slide.interval }}">
      <img src="{{ slide.image | prepend: site.baseurl }}" class="d-block w-100" alt="{{ slide.alt }}" loading="lazy">
      <div class="carousel-caption d-none d-md-block {% if slide.dark %}text-dark{% endif %}">
        <h5>{{ slide.title }}</h5>
        <p>{{ slide.subtitle }}</p>
      </div>
    </div>
    {% endfor %}
  </div>

  <!-- Carousel Controls -->
  <button class="carousel-control-prev" type="button" data-bs-target="#peracomSeminarCarousel2024" data-bs-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#peracomSeminarCarousel2024" data-bs-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
  </button>
</div>
</div>
---
Posters from our previous seminars in 2023:
<div class="d-flex justify-content-center">
<!-- Seminar Posters Carousel -->
<div id="peracomSeminarCarousel2023" class="carousel slide w-50" data-bs-ride="carousel">
  <div class="carousel-inner">
    {% for slide in site.data.peracom_seminars.carousel2023 %}
    <div class="carousel-item{% if forloop.first %} active{% endif %}" data-bs-interval="{{ slide.interval }}">
      <img src="{{ slide.image | prepend: site.baseurl }}" class="d-block w-100" alt="{{ slide.alt }}" loading="lazy">
      <div class="carousel-caption d-none d-md-block {% if slide.dark %}text-dark{% endif %}">
        <h5>{{ slide.title }}</h5>
        <p>{{ slide.subtitle }}</p>
      </div>
    </div>
    {% endfor %}
  </div>

  <!-- Carousel Controls -->
  <button class="carousel-control-prev" type="button" data-bs-target="#peracomSeminarCarousel2023" data-bs-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#peracomSeminarCarousel2023" data-bs-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
  </button>
</div>
</div>

---

### Watch Past Seminars

<div class="container">
  <div class="row justify-content-center">
    <div class="col-md-10 col-lg-8">
      <div class="ratio ratio-16x9">
        <iframe src="https://www.youtube.com/embed/Zex6tqiQdOg?si=VChu46vqJfwUzISB" title="YouTube video player" allowfullscreen></iframe>
      </div>
    </div>
  </div>
</div>

<p class="mt-4">
Recordings of the seminars are available on our <a href="https://www.youtube.com/playlist?list=PLPcJ5gOQ5iyWySopQpO3cZnSnrJ04NugP" target="_blank">YouTube Playlist</a>.
</p>


---

Peracom Seminars are a great opportunity to stay updated on the latest advancements in computer engineering and engage in discussions with experts from across the globe. Be sure to join us for the next session!