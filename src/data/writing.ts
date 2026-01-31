export interface Article {
  date: string;
  title: string;
  link: string;
  publication?: string;
}

export const articles: Article[] = [
  { date: "25-May-2021", title: "Difference Between Cohesion and Coupling", link: "https://www.baeldung.com/cs/cohesion-vs-coupling", publication: "Baeldung" },
  { date: "24-Apr-2020", title: "A Guide to jpackage in Java 14", link: "https://www.baeldung.com/java14-jpackage", publication: "Baeldung" },
  { date: "17-May-2019", title: "String API Updates in Java 12", link: "https://www.baeldung.com/java12-string-api", publication: "Baeldung" },
  { date: "11-Mar-2019", title: "Serializing and Deserializing a List with Gson", link: "https://www.baeldung.com/gson-list", publication: "Baeldung" },
  { date: "01-Jan-2019", title: "Java 11 Nest Based Access Control", link: "https://www.baeldung.com/java-nest-based-access-control", publication: "Baeldung" },
  { date: "19-Dec-2018", title: "Java 11 String API Additions", link: "https://www.baeldung.com/java-11-string-api", publication: "Baeldung" },
  { date: "15-Dec-2018", title: "Java 11 Local Variable Syntax for Lambda Parameters", link: "https://www.baeldung.com/java-var-lambda-params", publication: "Baeldung" },
  { date: "15-Dec-2018", title: "Java 11 Single File Source Code", link: "https://www.baeldung.com/java-single-file-source-code", publication: "Baeldung" },
  { date: "04-Nov-2018", title: "Rate Limiting in Spring Cloud Netflix Zuul", link: "https://www.baeldung.com/spring-cloud-zuul-rate-limit", publication: "Baeldung" },
  { date: "04-Aug-2018", title: "Sample Application with Spring Boot and Vaadin", link: "https://www.baeldung.com/spring-boot-vaadin", publication: "Baeldung" },
  { date: "26-May-2018", title: "Guide to Java 10", link: "https://www.baeldung.com/java-10-overview", publication: "Baeldung" },
  { date: "16-May-2018", title: "Java 10 Performance Improvements", link: "https://www.baeldung.com/java-10-performance-improvements", publication: "Baeldung" },
  { date: "16-May-2018", title: "Java 10 LocalVariable Type-Inference", link: "https://www.baeldung.com/java-10-local-variable-type-inference", publication: "Baeldung" },
  { date: "07-Mar-2018", title: "A Guide to Streams in Java 8: In-Depth Tutorial with Examples", link: "https://stackify.com/streams-guide-java-8/", publication: "Stackify" },
  { date: "12-Feb-2018", title: "Priority-based Job Scheduling in Java", link: "https://www.baeldung.com/java-priority-job-schedule", publication: "Baeldung" },
  { date: "16-Jan-2018", title: "Java 8 StringJoiner", link: "https://www.baeldung.com/java-string-joiner", publication: "Baeldung" },
  { date: "08-Aug-2017", title: "Introduction to gRPC", link: "https://www.baeldung.com/grpc-introduction", publication: "Baeldung" },
  { date: "23-Jul-2017", title: "Apache Commons Collections MapUtils", link: "https://www.baeldung.com/apache-commons-map-utils", publication: "Baeldung" },
];

// Group articles by publication
export function getArticlesByPublication(): Map<string, Article[]> {
  const byPublication = new Map<string, Article[]>();

  for (const article of articles) {
    const pub = article.publication || 'Other';
    if (!byPublication.has(pub)) {
      byPublication.set(pub, []);
    }
    byPublication.get(pub)!.push(article);
  }

  return byPublication;
}

// Get total count
export function getTotalArticles(): number {
  return articles.length;
}
