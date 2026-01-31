export interface Book {
  year: string;
  title: string;
  link: string;
  review?: string;
}

export const books: Book[] = [
  { year: "2025", title: "Project Hail Mary", link: "https://a.co/d/25Y5rHA" },
  { year: "2025", title: "Fish!: A Remarkable Way To Boost Morale And Improve Results", link: "https://a.co/d/cbiB2dj" },
  { year: "2024", title: "Amp It Up", link: "https://www.amazon.com/Amp-Unlocking-Hypergrowth-Expectations-Intensity/dp/1119836115" },
  { year: "2024", title: "Foundation", link: "https://www.amazon.com/gp/product/B000FC1PWA" },
  { year: "2024", title: "The Coaching Habit", link: "https://www.amazon.com/Coaching-Habit-Less-Change-Forever/dp/0978440749" },
  { year: "2024", title: "Designing Data-Intensive Applications", link: "https://www.amazon.com/Designing-Data-Intensive-Applications-Reliable-Maintainable/dp/1449373321" },
  { year: "2024", title: "Foundation and Empire", link: "https://www.amazon.com/gp/product/B000FC1PWA" },
  { year: "2023", title: "Mistborn: The Well of Ascension", link: "https://www.amazon.com/Well-Ascension-Book-Two-Mistborn-ebook/dp/B000UZQI0Q" },
  { year: "2023", title: "Mistborn: Hero of Ages", link: "https://www.amazon.com/Hero-Ages-Book-Three-Mistborn/dp/1250868319" },
  { year: "2022", title: "$100M Offers: How To Make Offers So Good People Feel Stupid Saying No", link: "https://www.amazon.com/100M-Offers-People-Stupid-Saying-ebook/dp/B099QVG1H8" },
  { year: "2022", title: "Mistborn: The Final Empire", link: "https://www.amazon.com/Mistborn-Final-Empire-Brandon-Sanderson/dp/0765377136" },
  { year: "2022", title: "Turn the Ship Around!: A True Story of Turning Followers into Leaders", link: "https://www.amazon.com/Turn-Ship-Around-Turning-Followers/dp/B08V4TFFCK" },
  { year: "2021", title: "Dune", link: "https://www.amazon.com/Dune-Sequence-Book-1-ebook/dp/B004KA9UXO" },
  { year: "2021", title: "Cognitive Behavioral Therapy Made Simple", link: "https://www.amazon.com/-/de/dp/1939754852" },
  { year: "2021", title: "Eat That Frog!", link: "https://www.amazon.com/Eat-That-Frog-Great-Procrastinating/dp/162656941X" },
  { year: "2020", title: "Atomic Habit", link: "https://www.amazon.com/Atomic-Habits-Proven-Build-Break/dp/0735211299" },
  { year: "2020", title: "Radical Candor", link: "https://www.amazon.com/Radical-Candor-Revised-Kick-Ass-Humanity/dp/1250235375" },
  { year: "2020", title: "Zero to One", link: "https://www.amazon.com/Zero-One-Notes-Startups-Future/dp/0804139296" },
  { year: "2020", title: "The Hitchhiker's Guide to the Galaxy", link: "https://www.amazon.com/Hitchhikers-Guide-Galaxy-Douglas-Adams/dp/0345418913" },
  { year: "2020", title: "The Restaurant at the End of the Universe", link: "https://www.amazon.com/gp/product/B001ODEQCU" },
  { year: "2019", title: "Black Swan", link: "https://www.amazon.com/Black-Swan-Improbable-Robustness-Fragility/dp/081297381X" },
  { year: "2018", title: "So Good They Can't Ignore You", link: "https://www.amazon.com/gp/product/1455509124", review: "/blog/so-good-they-cant-ignore-you/" },
  { year: "2018", title: "The 4-Hour Work Week", link: "https://www.amazon.com/gp/product/0091929113" },
  { year: "2018", title: "The Lessons Of History", link: "https://www.amazon.com/gp/product/143914995X" },
  { year: "2018", title: "On The Shortness Of Life", link: "https://www.amazon.com/gp/product/B00UMAQLG0" },
  { year: "2017", title: "Sapiens", link: "https://www.amazon.com/gp/product/0062316095" },
  { year: "2017", title: "Being Hindu", link: "https://www.amazon.com/gp/product/0143425323" },
  { year: "2017", title: "1984", link: "https://www.amazon.com/gp/product/0451524934" },
  { year: "2017", title: "Learned Optimism", link: "https://www.amazon.com/gp/product/1400078393" },
  { year: "2016", title: "The Fountainhead", link: "https://www.amazon.com/gp/product/0451191153" },
  { year: "2016", title: "Your Brain at Work", link: "https://www.amazon.com/gp/product/0061771295" },
  { year: "2016", title: "Search Inside Yourself", link: "https://www.amazon.com/gp/product/0062116932" },
  { year: "2016", title: "Brain Rules", link: "https://www.amazon.com/gp/product/098326337X" },
  { year: "2016", title: "Masters of Doom", link: "https://www.amazon.com/gp/product/0812972155" },
  { year: "Earlier", title: "Prakashvata", link: "https://www.amazon.in/gp/product/B00IBYD0QS", review: "/blog/book-review-prakashvata/" },
  { year: "Earlier", title: "The Lean Startup", link: "https://www.amazon.com/gp/product/0307887898", review: "/blog/book-review-lean-startup/" },
  { year: "Earlier", title: "The Last Lecture", link: "https://www.amazon.com/gp/product/1401323251" },
  { year: "Earlier", title: "The E-myth Revisited", link: "https://www.amazon.com/gp/product/0887307280" },
  { year: "Earlier", title: "The 7 Habits of Highly Effective People", link: "https://www.amazon.com/gp/product/1451639619" },
  { year: "Earlier", title: "The Naked Ape", link: "https://www.amazon.com/gp/product/0385334303" },
  { year: "Earlier", title: "C++ Primer", link: "https://www.amazon.com/gp/product/0321714113" },
  { year: "Earlier", title: "To Kill a Mockingbird", link: "https://www.amazon.com/gp/product/0446310786" },
  { year: "Earlier", title: "Shantaram", link: "https://www.amazon.com/gp/product/0312330537" },
  { year: "Earlier", title: "A Christmas Carol", link: "https://www.amazon.com/gp/product/0486268659" },
  { year: "Earlier", title: "The Catcher in the Rye", link: "https://www.amazon.com/gp/product/0316769487" },
  { year: "Earlier", title: "How to Win Friends & Influence People", link: "https://www.amazon.com/gp/product/0671027034" },
  { year: "Earlier", title: "Mrityunjay", link: "https://www.amazon.in/gp/product/8184984111" },
  { year: "Earlier", title: "Yayati", link: "https://www.amazon.in/gp/product/8171615880" },
  { year: "Earlier", title: "Duniyadari", link: "https://www.amazon.in/gp/product/B00I6ES8NI" },
  { year: "Earlier", title: "Partner", link: "https://www.amazon.in/gp/product/8177664298" },
  { year: "Earlier", title: "Shyamchi Aai", link: "https://www.amazon.in/gp/product/8177866591" },
  { year: "Earlier", title: "Apurvai", link: "https://www.amazon.in/gp/product/B073M7L3CV" },
  { year: "Earlier", title: "Vyakti Ani Valli", link: "https://www.amazon.in/gp/product/8174868984" },
  { year: "Earlier", title: "The White Tiger", link: "https://www.amazon.com/gp/product/1416562605" },
  { year: "Earlier", title: "Love Story", link: "https://www.amazon.com/gp/product/0380017601" },
  { year: "Earlier", title: "Effective C++", link: "https://www.amazon.com/gp/product/0321334876" },
  { year: "Earlier", title: "SCJP", link: "https://www.amazon.com/gp/product/0071591060" },
  { year: "Earlier", title: "Who Moved My Cheese", link: "https://www.amazon.com/gp/product/0399144463" },
  { year: "Earlier", title: "The Richest Man in Babylon", link: "https://www.amazon.com/gp/product/0451205367" },
  { year: "Earlier", title: "Rich Dad Poor Dad", link: "https://www.amazon.com/gp/product/1612680011" },
  { year: "Earlier", title: "Getting Things Done", link: "https://www.amazon.com/gp/product/0143126563" },
  { year: "Earlier", title: "Blink", link: "https://www.amazon.com/gp/product/0316010669" },
  { year: "Earlier", title: "Outliers", link: "https://www.amazon.com/gp/product/0316017930" },
  { year: "Earlier", title: "A Tour of C++", link: "https://www.amazon.com/gp/product/0321958314" },
  { year: "Earlier", title: "The Alchemist", link: "https://www.amazon.com/gp/product/0062315005" },
];

// Group books by year
export function getBooksByYear(): Map<string, Book[]> {
  const byYear = new Map<string, Book[]>();

  // Get unique years in order
  const years = [...new Set(books.map((b) => b.year))];

  for (const year of years) {
    byYear.set(year, books.filter((b) => b.year === year));
  }

  return byYear;
}

// Get total count
export function getTotalBooks(): number {
  return books.length;
}
