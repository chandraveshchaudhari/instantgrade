// src/config/config.ts

export const getAsset = (path: string) => {
  return `${process.env.NEXT_PUBLIC_BASE_PATH || ''}/${path}`;
};

const siteConfig = {
  personal: {
    name: 'Prachi Shah',
    title: 'Economics & Data Science Student | Christ University',
    image: getAsset('images/profile.png'),
    description:
      'B.Sc. Economics with Data Science student at Christ (Deemed to be University), BRC Campus. ' +
      'Passionate about data analysis, critical thinking, and turning numbers into meaningful insights.\n' +
      '\n' +
      'Actively involved in club activities, debating, and leadership roles that sharpen both analytical and communication skills.\n' +
      '\n' +
      'Completed the Young Changemakers Programme at IIM Ranchi and hold a creative writing certification.\n' +
      '\n' +
      'Proud youngest female black belt in the district — discipline and resilience carry over into everything I do.',
    tagline: 'Turning data into decisions, one insight at a time.',
    location: 'India',
  },

  seo: {
    title: 'Prachi Shah – Economics & Data Science Student',
    description: 'Portfolio website showcasing education, projects, experience, and skills of Prachi Shah.',
  },

  animatedText: ['Data Analyst', 'Economics Student', 'Content Writer', 'Problem Solver'],

  navigation: [
    { name: 'Home', url: '/' },
    { name: 'Projects', url: '/projects' },
    { name: 'Research', url: '/research' },
    { name: 'Education', url: '/education' },
    { name: 'Experience', url: '/experience' },
    { name: 'Blogs', url: '/blogs' },
    { name: 'Resume', url: '/resume' },
    { name: 'Contact', url: '/contact' },
  ],

  blogs: [
    {
      title: 'Your Blog Title',
      url: getAsset('static_page/project_management_blog.html'),
    },
  ],

  education: [
    {
      institution: 'Christ (Deemed to be University), BRC Campus',
      degree: 'B.Sc. Economics with Data Science',
      year: '2024–Present',
      image: getAsset('images/education/placeholder.png'),
      description: [
        'First Year student with a GPA of 3.72 / 4.0 (Semester 1).',
        'Coursework includes advanced Excel, introductory Python, and foundational data workflows.',
      ],
    },
    {
      institution: 'Eklavya Global School',
      degree: 'Secondary Education',
      year: 'Up to 2024',
      image: getAsset('images/education/placeholder.png'),
      description: [
        'Served as Head Girl — managed student responsibilities and organised large-scale events.',
      ],
    },
  ],

  certifications: [
    {
      title: 'Creative Writing Certification',
      file: getAsset('images/education/Certifications/download.svg'),
    },
    {
      title: 'Young Changemakers Programme – IIM Ranchi',
      file: getAsset('images/education/Certifications/download.svg'),
    },
  ],

  experience: [
    {
      title: 'Young Changemakers Programme',
      cardImage: getAsset('images/experience/placeholder.png'),
      place: 'IIM Ranchi',
      time: '(Dec 2024)',
      desp: [
        'Solved real-world problems collaboratively within strict timelines.',
        'Improved critical thinking and enhanced collaboration and leadership skills.',
      ],
    },
    {
      title: 'Literary Committee Member',
      cardImage: getAsset('images/experience/placeholder.png'),
      place: 'Student Welfare Office – Christ University',
      time: '(2024–Present)',
      desp: [
        'Produced written material under tight deadlines across formal and creative formats.',
        'Worked within a structured student-administration setting.',
      ],
    },
    {
      title: 'Economics & Data Science Club Member',
      cardImage: getAsset('images/experience/placeholder.png'),
      place: 'Christ University',
      time: '(2024–Present)',
      desp: [
        'Gained foundational Python skills and learned introductory data workflows.',
      ],
    },
    {
      title: 'MUN Delegate',
      cardImage: getAsset('images/experience/placeholder.png'),
      place: 'External Debating Society',
      time: '(2024–Present)',
      desp: [
        'Developed rapid research capabilities and delivered structured, professional arguments.',
        'Explored international policy issues through Model United Nations simulations.',
      ],
    },
    {
      title: 'Head Girl',
      cardImage: getAsset('images/experience/placeholder.png'),
      place: 'Eklavya Global School',
      time: '(2023–2024)',
      desp: [
        'Managed student responsibilities and handled high-pressure situations.',
        'Single-handedly organised an event for more than 100 teachers, strengthening organisational skills.',
      ],
    },
  ],

  projects: [
    {
      title: 'Interactive Excel Dashboard',
      cardImage: getAsset('images/project/placeholder.png'),
      description:
        'Built interactive dashboards using advanced Excel functions for coursework and Economics & Data Science Club tasks. Focused on visual data storytelling and real-time analysis.',
      Githublink: 'https://github.com/your-username/your-project', // Replace with your actual repo link
    },
  ],

  research: [
    {
      title: 'Your Paper or Research Title',
      authors: 'Prachi Shah',
      conferences: 'Conference or Journal, Publisher',
      researchYr: 2024,
      image: getAsset('images/research/placeholder.png'),
      citation: {
        vancouver: 'Shah P. Title of the work. Venue, Year. DOI/URL.',
      },
      abstract: 'One or two sentences summarizing the contribution...',
      link: 'https://example.com/your-publication',
    },
  ],

  books: [
    {
      title: 'Your Book Title',
      description: 'Short description of your book or resource.',
      image: getAsset('images/book_cover_placeholder.png'),
      link: 'https://example.com/your-book',
    },
  ],

  contact: {
    email: 'findprachishah@gmail.com',
    linkedin: 'https://www.linkedin.com/in/your-linkedin/',   // Replace with your LinkedIn URL
    github: 'https://github.com/your-username',                // Replace with your GitHub URL
    googleScholar: 'https://scholar.google.com/citations?user=YOURID', // Replace if applicable
    orcid: 'https://orcid.org/0000-0000-0000-0000',            // Replace if applicable
  },
};

export default siteConfig;
