export interface Video {
  title: string;
  link: string;
  comment: string;
  thumbnail?: string;
}

export const videos: Video[] = [
  {
    title: "A Class Divided",
    link: "https://www.pbs.org/wgbh/frontline/film/class-divided/",
    comment: "Had a profound effect on me. Better understood discrimination and its effects. If there is any need for schooling in its current form, it is for such kind of activities.",
  },
  {
    title: 'Swami Sarvapriyananda - "Secret of Concentration" at IIT Kanpur',
    link: "https://www.youtube.com/watch?v=BGswR0tMqCM&t=261s",
    comment: "Nicely connects the teachings of Yoga and Positive Psychology on the topic of flow",
  },
  {
    title: "Naval Ravikant | The Angel Philosopher",
    link: "https://www.youtube.com/watch?v=mGY2To_HW98",
    comment: "Naval Ravikant on The Knowledge Project podcast with Shane Parrish. Episode that introduced me to Naval.",
  },
  {
    title: "Inside the mind of a master procrastinator",
    link: "https://www.youtube.com/watch?v=arj7oStGLkU",
    comment: "Popular and funny TED talk on procrastination with a very important point to make.",
  },
];

// Extract YouTube video ID from URL
export function getYouTubeId(url: string): string | null {
  const regex = /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/;
  const match = url.match(regex);
  return match ? match[1] : null;
}

// Get YouTube thumbnail URL
export function getYouTubeThumbnail(url: string): string | null {
  const id = getYouTubeId(url);
  return id ? `https://img.youtube.com/vi/${id}/mqdefault.jpg` : null;
}
