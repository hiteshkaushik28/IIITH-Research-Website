from app import app
from flask import render_template

# route for labs page
@app.route('/labs')
def labs():
	lab = [
		{
			'lab_id': '1',
			'name': 'Kohli Center on Intelligent Systems (KCIS)',
			'url': 'http://kcis.iiit.ac.in',
			'info': '<p><strong>Kohli Center on Intelligent Systems</strong> (KCIS) was established at <strong>International Institute of Information Technology, Hyderabad</strong> (IIIT Hyderabad) in 2015 with funding from <strong>Tata Consultancy Services</strong> (TCS) to give a fillip to research, teaching and entrepreneurship in the broad Intelligent Systems area.</p>'
		},
		{
			'lab_id': '2',
			'name': 'Signal Processing and Communications Research Center (SPCRC)',
			'url': 'http://spcrc.iiit.ac.in/',
			'info': '<p>SPCRC was set up in 2003 with the goal of undertaking fundamental research in signal processing and communication engineering. Research, at theoretical and applied levels, is conducted in this center. Funding sources have included MCIT, DST, GE Global Research, Bangalore etc.</p>'
		},
		{
			'lab_id': '3',
			'name': 'Data Sciences and Analytics Center (DSAC)',
			'url': 'http://dsac.iiit.ac.in/',
			'info': '<p>Data Sciences and Analytics Center conducts research, facilitates technology transfer, and builds systems in the broad area of data engineering. The center inculcates the culture of research in students by involving them in activities such as:</p>'


		},
		{
			'lab_id': '4',
			'name': 'Language Technologies Research Center (LTRC)',
			'url': 'http://ltrc.iiit.ac.in/',
			'info': '<p>The LTRC addresses the complex problem of understanding and processing natural languages in both speech and text modes.</p><ul><li>LTRC conducts research on both basic and applied aspects of language technology.</li><li>It is the largest academic centre of speech and language technology in India.</li><li>LTRC carries out its work through four labs, which work in synergy with each other.</li></ul><p>LTRC is also a lead participant in nation-wide mission-mode consortia projects to develop deployable technology in the areas of Indian Language Machine Translation, English to Indian Language Machine Translation, and Cross Language Information Access (search engines).</p><h4>NLP-MT Lab</h4><p>The NLP-MT lab does fundamental work on developing grammatical as well statistical modelling of languages. Linguistic approaches are combined with machine learning techniques leading to new theories and technology development. This has resulted in higher accuracy parts-of-speech taggers, chunkers, constraint-based parsers as well as broad coverage statistical parsers, and semantic analyzers for Indian languages on the one hand, and annotated data including dependency tree banks, discourse banks, parallel corpora, etc. on the other.</p><h4>Anusaaraka Lab</h4><p>Anusaaraka lab is concerned with the development of machine translation systems which in addition to the usual machine translation output also allows a user to understand the source language text in a pseudo target language. For example, a reader who knows Hindi (target language) would be able to read the English source text, in a pseudo Hindi output after a small amount of training.</p>'
		},
		{
			'lab_id': '5',
			'name': 'Robotics Research Center (RRC)',
			'url': 'http://robotics.iiit.ac.in/',
			'info': '<p>The IIIT-H Robotics Research Lab works on research problems and innovative projects that extend the state-of-the-art in robotics. The center has worked in multiple domains of robotics involving Multi-robotic systems, Mobile robot navigation and planning, Mechanism design of All Terrain Vehicles and Robot Vision. The lab is well equipped with robot platforms and advanced sensors and has been publishing in top international conferences like ICRA, IROS, ICCV, AAMAS. The center is being and has been funded by various organizations both private, public and government. These include BARC, CAIR, Renault-Nissan, CVRDE, DRDO, DST, DIT and by IIIT Seed Grants The Robotics Research Center also collaborates with well known organizations and research labs such as CAIR, Bengaluru and BARC, Mumbai.</p><p><strong>Resources and Infrastructure:</strong> The lab is equipped with various robot test beds that are used in the research. These include ground robots like the pioneer P3-DX, the all terrain P3-AT along with the aerial robots like the parrot and the pelican. Along with these robots it is also equipped with a wide range of cameras and sensors.</p><p><strong>Mobile Robotics: </strong>Localization, mapping and navigation of robots in indoors and outdoor environments.</p><p><strong>Robot Mechanisms:</strong> Mechanical design and analysis of all-terrain vehicles.</p><p><strong>Multi Robots:</strong> Exploration and localization using multiple robots.</p><p><strong>Robotic Vision: </strong>Vision Processing algorithms for localization, mapping and classification.</p><h4>Current Research Areas</h4><div><p><strong>Robotic Vision</strong></p><ul><li>Independent Motion Detection and Segmentation</li><li>Monocular SLAM in Dynamic Environments</li><li>Monocular Localization</li><li>Structure Aided Visual SLAM</li><li>Visual Servoing for Space Robots</li></ul><p><strong>Multi Robotic Systems</strong></p><ul><li>Ground-Aerial Vehicle Coordination</li><li>Multi Robotic Exploration</li><li>Multi Robotic Collision Avoidance</li></ul><p><strong>Mobile and Embedded Robotics</strong></p><ul><li>Semantically Navigated Wheel Chair Systems</li><li>Object Search and Localization</li><li>FPGA Architectures for Mobile Robots</li></ul><p><strong>Mechanism Design</strong></p><ul><li>Active and Passive Mechanisms for All Terrain Navigation</li><li>Quadruped and Biped Design and Fabrication</li><li>Gait Generation for Quadruped and Wheeled Legged Systems</li></ul></div><h4>Faculty</h4><ul><li>Madhava Krishna K.</li><li>Rambabu Kalla</li><li>Suril Vijaykumar Shah</li></ul>'
		},
		{
			'lab_id': '6',
			'name': 'Center for Security, Theory and Algorithms (CSTAR)',
			'url': 'http://web2py.iiit.ac.in/research_centres/default/view_area/6',
			'info': '<p>The goal of the center is to do research in information security, theory and algorithms. It also participates in teaching various programmes of the Institute by offering various mandatory and elective courses in the areas of theoretical computer science and information security.</p><p>The center runs an M.Tech in CSIS (Computer Science &amp; Information Security) with support from MCIT Government of India (Ministry of Communications &amp; Information Technology) and participates in programmes of the Institute such as PhD / MS / Dual degree etc. with a specialization in algorithms, theoretical computer Science or information security. The center aspires to be</p><ul><li>A resource center for conceptualizing through fundamental insights</li><li>A knowledge center for effectively imparting the state-of-the-art in Theoretical computer Science and in Information Security</li><li>An accessible medium for disseminating and sharing expertise towards scientific and societal impact</li></ul><h4>Current Research Areas</h4><ul><li>System and network security</li><li>Security issues in wireless sensor networks</li><li>Multicore and manycore computing</li><li>Quantam information theory</li><li>Quantam information processing</li><li>Distributed graph algorithms</li><li>Cryptography</li><li>Geometric algorithms and data structures for large scale VLSI layouts</li></ul><h4>Faculty</h4><ul><li>Ashok Kumar Das</li><li>Bezawada Bruhadeshwar</li><li>Indranil Chakrabarty</li><li>Kannan Srinathan</li><li>Kishore Kothapalli</li><li>Shatrunjay Rawat</li></ul>'
		},
		{
			'lab_id': '7',
			'name': 'Software Engineering Research Center (SERC)',
			'url': 'https://serc.iiit.ac.in/',
			'info': '<p>Software engineering is the engineering of large and complex software systems. It focuses on systematic, disciplined, quantifiable approach to the development, operation, and maintenance of quality software, and the study of these approaches. SERC aims to lead the software engineering research in India by addressing India-specific issues in an industry-driven environment.</p><p>The main objectives of SERC are to focus on software engineering research, research in software engineering issues in the context of Indian software industry, operate closely with the industry by establishing touch points and to be a center of excellence driven by the industry for the industry.</p><p>Some of the major funded projects are state variable approach to the model-driven development of software for reactive systems (funded by SIEMENS), virtual Labs Integration (funded by MHRD), standardization of mobile interfaces (funded by CA Technologies) and big data analytics on the cloud (funded by CA Technologies).</p><h4>Current Research Areas</h4><ul><li>Software architectures and software reuse</li><li>Software engineering education</li><li>Programming languages</li><li>Mathematical computer science and formal methods</li><li>Technology for education</li><li>Model driven development</li><li>Process engineering</li><li>Semantic web architectures</li><li>Human computer interaction</li></ul><h4>Faculty</h4><ul><li>Kesav V. Nori</li><li>Raghu Reddy Y.</li><li>Ramesh Loganathan</li><li>Vasudeva Varma</li><li>Venkatesh Choppella</li><li>Viswanath K.</li><li>Suresh Purini</li></ul>'
		},
		{
			'lab_id': '8',
			'name': 'Center for Visual Information Technology (CVIT)',
			'url': 'http://cvit.iiit.ac.in/',
			'info': '<p>CVIT focuses on basic and advanced research in image processing, computer vision, computer graphics and machine learning. This center deals with the generation, processing, and understanding of primarily visual data as well as with the techniques and tools required doing so efficiently. The activity of this center overlaps the traditional areas of Computer Vision, Image Processing, Computer Graphics, Pattern Recognition and Machine Learning. CVIT works on both theoretical as well as practical aspects of visual information processing. Center aims to keep the right balance between the cutting edge academic research and impactful applied research.</p><p>Research projects are funded by various agencies like- Department of Science and Technology (DST), Naval Research Board (NRB), Ministry of Communications and Information Technology (MCIT), Defence Research and Development Organisation (DRDO), General Electric (GE), Nvidia and many more.</p><p>CVIT has around 50 students carrying out research for M.S. and Ph.D. degrees.</p><p>The center has regular visits and talks by leading researchers in the world.</p><h4>Current Research Areas</h4><ul><li>Document image processing especially recognition and retrieval</li><li>Biomedical and retinal image processing to aid doctors in diagnosis</li><li>Biometrics based on palm prints, handwriting, and hand geometry</li><li>Content-based annotation and search of large collections of images and videos</li><li>Machine learning for computer vision</li><li>Real-time rendering and streaming of large geometry including terrains and developing general purpose applications on the graphics processor units (GPUs) including graph algorithms, computer vision, and pattern recognition</li></ul><h4>Faculty</h4><ul><li>Anoop Namboodiri</li><li>Jawahar C. V.</li><li>Jayanthi Sivaswamy</li><li>Narayanan P. J.</li><li>Vineet Gandhi</li><li>Avinash Sharma</li></ul>'
		},
		{
			'lab_id': '9',
			'name': 'Center for VLSI and Embedded Systems Technology (CVEST)',
			'url': 'http://web2py.iiit.ac.in/research_centres/default/view_area/9',
			'info': '<p>The Center works in close collaboration with organizations such as Xilinx, Altera, Intel Corporation, DRDO etc. The center has three labs under its supervision - VLSI CAD Lab comprising of state-of-the-art VLSI CAD tools like CADENCE tools suite - Embedded Systems Lab-1 equipped with ARM Processor kits, ATMEGA8 and ATMEGA32 boards - Embedded Systems Lab-2 equipped with Altera FPGA Boards, TI Mixed Signal System Development kit, Intel Atom Processor boards. The facilities are available for all Institute staff and students who would like to participate in VLSI R&amp;D activity.</p><h4>Current Research Areas</h4><ul><li>Low power VLSI design</li><li>VLSI architectures</li><li>Biomedical embedded systems</li><li>Analog and mixed signal design</li><li>High speed communications in VLSI circuits</li><li>Multicore (Processor) architecture for embedded systems</li><li>ME, MS and MEM TRONICS</li><li>FPGA based embedded systems</li></ul><h4>Faculty</h4><ul><ul><li>Govindarajulu R.</li><li>Shubhajit Roy Chowdhury</li><li>Suresh Purini</li><li>Syed Azeemuddin</li></ul></ul><ul><li>Vijaya Sankara Rao P.</li></ul>'
		},
		{
			'lab_id': '10',
			'name': 'Computer Systems Group(CSG)',
			'url': 'http://csg.iiit.ac.in/',
			'info': '<p>The Computer Systems Group (CSG) was set-up in June 2017. Computer Systems Group undertakes research and development in all fundamental aspects of Computing Systems spanning across hardware and software. This group is actively involved in research and imparting advanced training through workshops, seminars, and semester long courses in the fields of computer architecture, compilers, computer networks, operating systems and other related topics. As a new group CSG today has about 3 faculty members and about 15 research students including Phd, Masters and honors students working on research topics that directly contribute and make an impact on the next-generation computing hardware and software.</p><h4>Current Research Areas</h4><ul><li>Computer Architecture</li><li>Compilers</li><li>Programming Languages</li><li>Computer Networks</li><li>Parallel and Distributed Computing</li><li>Cloud Computing</li><li>Systems Security</li><li>Internet of Things</li></ul><h4>Faculty</h4><ul><li>Suresh Purini</li><li>Venkatesh Choppella</li><li>Lavanya Ramapantulu</li></ul>'
		}
	]
	return render_template('labs.html', lab=lab)
