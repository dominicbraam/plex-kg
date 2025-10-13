# Pre-requisite Knowledge

This project was done to help understand the semantic web and this document will include important things to remember.

> [!NOTE]
> This document is made up of mostly direct quotes.

## Semantic Web

The Semantic Web is a vision about an **extension** of the existing World Wide Web, which provides software programs with **machine-interpretable metadata** of the published information and data. In other words, we add further data descriptors to otherwise existing content and data on the Web. As a result, computers are able to **make meaningful interpretations** similar to the way humans process information to achieve their goals.

The ultimate ambition of the Semantic Web, as its founder **Tim Berners-Lee** sees it, is to enable computers to better manipulate information on our behalf. He further explains that, in the context of the Semantic Web, the word **“semantic” indicates machine-processable** or what a machine is able to do with the data. Whereas **“web” conveys the idea of a navigable space of interconnected objects** with mappings from URIs to resources.

## Ontologies

An ontology is a formal description of knowledge as **a set of concepts** within a domain **and the relationships** that hold between them. To enable such a description, we need to formally specify components such as individuals (instances of objects), classes, attributes and relations as well as restrictions, rules, and axioms. As a result, ontologies do not only introduce a shareable and reusable knowledge representation but can also add new knowledge about the domain.

The ontology data model can be applied to a set of individual facts to create a **knowledge graph** – a collection of entities, where the types and the relationships between them are expressed by nodes and edges between these nodes. By describing the structure of the knowledge in a domain, the ontology sets the stage for the knowledge graph to capture the data in it.

### Real Life Examples

- DBpedia, which extracts structured content from Wikipedia and represents it using ontologies for advanced querying and data analysis.
- FOAF (Friend Of A Friend), describes people and social relationship on the Web.
- Gene Ontology (GO), used in bioinformatics for unifying the representation of gene and protein functions across species.

## Linked Data Principles

- Use RDF as data format.
- Use HTTP URIs as names for things so that people can look up those names.
- When someone looks up a URI, provide useful information (RDF, HTML, etc.) using content negotiation.
- Include links to other URIs so that related things can be discovered.

**Additional Notes**

- If it doesn't use the universal URI set of symbols, we don't call it Semantic Web.
- HTTP URIs are names (not addresses) and HTTP name lookup is a complex, powerful and evolving set of standards.
- One can, in general, look up the properties and classes one finds in data, and get information from the RDF, RDFS, and OWL ontologies including the relationships between the terms in the ontology. The basic format here for RDF/XML, with its popular alternative serialization N3 (or Turtle). Large datasets provide a SPARQL query service, but the basic linked data should be provided as well.
- Making links to other things is necessary to connect the data we have into a web, a serious, unbounded web in which one can find all kinds of things, just as on the hypertext web we have managed to build.

## RDF (Resource Description Framework)

- Framework for describing resources on the web.
- Designed to be read and understood by computers.
- Written in XML. The XML language used by RDF is called RDF/XML.
- Uses Web identifiers (URIs) to identify resources.
- Describes resources with properties and property values.
    - A **resource** is anything that can have a URI, such as "https://www.w3schools.com/rdf"
    - A **property** is a resource that has a name, such as "author" or "homepage"
    - A **property** value is the value of a property, such as "Jan Egil Refsnes" or "https://www.w3schools.com" (note that a property value can be another resource)
- The combination of a resource, a property, and a property value forms a **statement** (known as the subject, predicate, and object of a statement).
    - **Statement:** "The homepage of https://www.w3schools.com/rdf is https://www.w3schools.com".
        - **Subject:** https://www.w3schools.com/rdf
        - **Predicate:** homepage
        - **Object:** https://www.w3schools.com
- Use the [online converter](https://www.easyrdf.org/converter) to convert/validate your RDF files.

**Languages/Syntax:**

- **XML/RDF:** The oldest RDF format is RDF/XML which is not used as often anymore but is still standard due to this fact. This means that most RDF libraries and triplestores output RDF in this format by default. Syntax basics: [XML RDF](https://www.w3schools.com/xml/xml_rdf.asp).
- **Turtle:** Reading (as a human) RDF in Turtle format is much easier as you can define prefixes at the beginning of the .ttl file, shortening each triple. Another feature of turtle is that multiple triples with the same subject are grouped into blocks (so the URI for Bob Marley for example is not repeatedly listed). Syntax basics: [Turtle syntax basics](https://learnxinyminutes.com/rdf/)

## Resources

- [Linked Data](https://www.w3.org/DesignIssues/LinkedData.html)
- [Ontologies](https://www.lyzr.ai/glossaries/ontologies/)
- [understanding Linked Data Formats](https://medium.com/wallscope/understanding-linked-data-formats-rdf-xml-vs-turtle-vs-n-triples-eb931dbe9827)
- [What Are Ontologies?](https://www.ontotext.com/knowledgehub/fundamentals/what-are-ontologies/?utm_source=chatgpt.com)
- [What Is the Semantic Web?](https://www.ontotext.com/knowledgehub/fundamentals/what-is-the-semantic-web/)
- [XML RDF](https://www.w3schools.com/xml/xml_rdf.asp)
