#set page(
  paper: "a4",
  margin: (x: 1.5cm, y: 1.2cm),
)
#set text(
  font: "Inter",
  size: 10pt,
  fill: rgb("#2d3748"),
  spacing: 120%,
)

// Define colors
#let primary-color = rgb("#1a365d") // Deep Navy
#let secondary-color = rgb("#2b6cb0") // Slate Blue
#let text-color = rgb("#2d3748") // Charcoal
#let line-color = rgb("#cbd5e0") // Light Grey

#set text(fill: text-color)

// Header
#align(center)[
  #text(size: 22pt, weight: "bold", fill: primary-color)[Fani Bhushan] \
  #v(2pt)
  #text(size: 9.5pt, fill: text-color)[
    **Location:** Berlin, Germany | **Email:** fani.bhushan\@mercedes-benz.com
  ]
]

#v(4pt)
#line(length: 100%, stroke: 0.5pt + line-color)
#v(2pt)

// Section Helper
#let section(title) = {
  v(8pt)
  text(size: 12pt, weight: "bold", fill: primary-color)[#title]
  v(2pt)
  line(length: 100%, stroke: 1.5pt + primary-color)
  v(4pt)
}

// Professional Summary
#section("Professional Summary")
#text(size: 9.5pt)[
  Senior Technical Leader and Architect with 16+ years of experience in embedded systems, automotive infotainment, and connected car services. A proven track record of leading cross-functional teams, executing strategic product roadmaps as Acting Product Owner, and delivering high-impact software solutions. Highly skilled in aligning technical architecture with business strategy, resolving critical bug escalations, and mentoring engineers.
]

// Core Skills
#section("Core Skills & Competencies")
#v(2pt)
#grid(
  columns: (110pt, 1fr),
  row-gutter: 6pt,
  [*Programming Languages:*], [C++, Qt/QML, C\#, Golang, Java, Python, Kotlin(beginner)],
  [*Architectures & Systems:*], [Dialog Engines, Connected Car Platforms, Microservices, Containerization (Docker), Navigation system, Embedded Linux, Infotainment systems],
  [*Leadership & Methodologies:*], [Agile/Scrum, CSPO (Certified Scrum Product Owner), PI Planning, Line Management, Stakeholder Management, CI/CD, Automated Testing],
)

// Professional Experience
#section("Professional Experience")

#let job(role, company, date, location, details) = {{
  v(4pt)
  grid(
    columns: (1fr, auto),
    [*#role* \ #text(fill: secondary-color, weight: "medium")[#company]],
    [#text(size: 8.5pt, style: "italic")[#date] \ #align(right)[#text(size: 8.5pt, fill: rgb("#718096"))[#location]]]
  )
  v(2pt)
  for detail in details {{
    list(marker: [•], tight: true, [#detail])
  }}
}}

#job(
  "Expert Software Engineer / Acting Product Owner",
  "MBition GmbH (Mercedes-Benz Innovation)",
  "03/2018 – Present",
  "Berlin, Germany",
  (
    [*AI Integration \& Production Release:* Did the POC and led the actual development for production and delivered within deadline.],
    [*Product \& PI Leadership:* Served as Acting PO for Speech Assistant and MBUX Online Media. Handled PI planning, backlog, capacity, and stakeholder escalations.],
    [*Connected Car Services:* Architected and led the development of Qt/Golang/Java-based multi-platform connected car services and UI platforms for Mercedes-Benz.],
    [*Containerized Apps:* Managed end-to-end implementation and FOSS certification for speech container services and in-vehicle payment apps (_Fuel \& Pay_).],
    [*MBUX Infotainment UI:* Directed development of the Qt/C++ Online Media UI, collaborating with distributed international teams.]
  )
)

#job(
  "Software Technical Lead",
  "Wipro Technologies",
  "05/2010 – 01/2018",
  "Germany / Tokyo, Japan / Bangalore, India",
  (
    [*Line Management \& Leadership:* Managed engineering team career growth, performance evaluations, and resource planning.],
    [*On-site Client Coordination:* Directed stakeholder negotiations, onsite-offshore collaboration, and vehicle test drives in Germany and Japan (Panasonic).],
    [*UI Testing Tool Development:* Led development of a C\#-based UI testing tool integrated with Python and Perl for automated testing.],
    [*Navigation \& Firmware Systems:* Developed routing and route guidance components in C++, and firmware for smart meters and robotic vacuum cleaners using Embedded C and RTOS.]
  )
)
