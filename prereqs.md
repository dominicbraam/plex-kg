# Pre-requisite Knowledge

This project was done to help understand the semantic web and this document will include important things to remember.

> [!NOTE]
> This document is made up of mostly direct quotes.

## Semantic Web

The Semantic Web is a vision about an **extension** of the existing World Wide Web, which provides software programs with **machine-interpretable metadata** of the published information and data. In other words, we add further data descriptors to otherwise existing content and data on the Web. As a result, computers are able to **make meaningful interpretations** similar to the way humans process information to achieve their goals.

The ultimate ambition of the Semantic Web, as its founder **Tim Berners-Lee** sees it, is to enable computers to better manipulate information on our behalf. He further explains that, in the context of the Semantic Web, the word **“semantic” indicates machine-processable** or what a machine is able to do with the data. Whereas **“web” conveys the idea of a navigable space of interconnected objects** with mappings from URIs to resources.

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

## W3C Semantic Web Tech Stack

- **RDF**: data model for describing resources as triples.
- **SPARQL**: query language for retrieving and manipulating RDF data.
- **SHACL**: constraint language for validating RDF graph structure and values.
- **RDFS/OWL**: languages for defining and reasoning over RDF schemas and ontologies.
- **SKOS**: vocabulary for representing taxonomies and thesauri in RDF

### RDF (Resource Description Framework)

- Framework for describing resources on the web.
- Designed to be read and understood by computers.
- Written in XML. The XML language used by RDF is called RDF/XML.
- Uses Web identifiers (URIs) to identify resources.
- Describes resources with properties and property values.
    - A **resource** is anything that can have a URI, such as `https://www.w3schools.com/rdf`.
    - A **property** is a resource that has a name, such as "author" or "homepage".
    - A **property** value is the value of a property, such as "Jan Egil Refsnes" or `https://www.w3schools.com` (note that a property value can be another resource)
- The combination of a resource, a property, and a property value forms a **statement** (known as the subject, predicate, and object of a statement) - **aka. a Triple**.
    - **Statement:** "The homepage of `https://www.w3schools.com/rdf` is `https://www.w3schools.com`".
        - **Subject:** `https://www.w3schools.com/rdf`
        - **Predicate:** homepage
        - **Object:** `https://www.w3schools.com`
- Use the [online converter](https://www.easyrdf.org/converter) to convert/validate your RDF files.

**Languages/Syntax:**

- **XML/RDF:** The oldest RDF format is RDF/XML which is not used as often anymore but is still standard due to this fact. This means that most RDF libraries and triplestores output RDF in this format by default. Syntax basics: [XML RDF](https://www.w3schools.com/xml/xml_rdf.asp).
- **Turtle:** Reading (as a human) RDF in Turtle format is much easier as you can define prefixes at the beginning of the .ttl file, shortening each triple. Another feature of turtle is that multiple triples with the same subject are grouped into blocks (so the URI for Bob Marley for example is not repeatedly listed). Syntax basics: [Turtle syntax basics](https://learnxinyminutes.com/rdf/)

### SPARQL

SPARQL is used to query RDF datasets. The WHERE clause usually triples (subject, predicate, object). After writing that triple, it looks just like an example of the data you want returned. It is a very direct form of querying.

### SHACL

SHACL is used to describe what the RDF data should look like. It ensures the graph conforms to the expected structures and datatypes. ie. validation.

## Taxonomies

A taxonomy is a hierarchical framework, or schema, for the organization of organisms, inanimate objects, events, and/or concepts. We see taxonomies daily as humans, and we don’t give them much thought. Taxonomies are the facets, filters, and search suggestions commonly seen on modern websites.

For example, books can be categorized as fiction and nonfiction at a high level. That may work in some instances, but in most cases, that is too high of a grouping level, so we further subdivide each high-level category until we are satisfied we have achieved an appropriate grouping level.

## Ontologies

(classes, properties, axioms)

According to Wikipedia, an ontology “encompasses a representation, formal naming, and definition of the categories, properties, and relations between the concepts, data, and entities that substantiate one, many, or all domains of discourse.” In other words, ontologies allow us to organize the jargon of a subject area into a controlled vocabulary, thereby decreasing complexity and confusion. Without ontologies, you have no frame of reference, and understanding is lost. For example, an ontology will allow one to associate the Book taxonomy with the Customer taxonomy via relationships.

We need to formally specify components such as individuals (instances of objects), classes, attributes and relations as well as restrictions, rules, and axioms. As a result, ontologies do not only introduce a shareable and reusable knowledge representation but can also add new knowledge about the domain.

The ontology data model can be applied to a set of individual facts to create a **knowledge graph** – a collection of entities, where the types and the relationships between them are expressed by nodes and edges between these nodes. By describing the structure of the knowledge in a domain, the ontology sets the stage for the knowledge graph to capture the data in it.

**Real Life Examples:**

- DBpedia, which extracts structured content from Wikipedia and represents it using ontologies for advanced querying and data analysis.
- FOAF (Friend Of A Friend), describes people and social relationship on the Web.
- Gene Ontology (GO), used in bioinformatics for unifying the representation of gene and protein functions across species.

## Additional Takeaways

**Terms**:

- **URL**: URI that locates a resource on the web. eg. `https://dominicbraam.com/`
- **URI**: unique identifier for a resource. eg. `https://dominicbraam.com/projects/milo/`
    - Note that all URIs are URLs but URLs are not URIs.
- **IRI**: Unicode-enabled form of URI. eg. `https://dominicbraam.com/résumé`.
    - Can be used to represent URIs in languages that don't use the english alphabet.
- **Resource**: anything identifiable by a URI.
- **Namespace**: prefix that abbreviates IRIs.
- **Dereferencing**: fetching a resource’s data by accessing its URI.

**Hierarchy → Schema → Meaning → Data**:

- **Taxonomy**: hierarchical tree of categories using only “is-a” links.
- **Ontology**: semantic schema defining classes, properties, and relationships.
- **Semantic model**: formal representation of meaning in a domain, often implemented as an ontology.
- **Knowledge graph**: data layer built from instances (entities and relationships) that conform to a semantic model or ontology.

**Ontology facts:**

- an ontology may allow inferences on data that uses it
- conceptual graphs can represent an ontology
- a shared ontology promotes interoperability
- description logics can represent an ontology

## Resources

- [A Glance at SPARQL](https://youtu.be/GIK19zUlmVo?si=qtp_zuQOnXuYY4m6)
- [Linked Data](https://www.w3.org/DesignIssues/LinkedData.html)
- [Ontologies](https://www.lyzr.ai/glossaries/ontologies/)
- [Taxonomies, Ontologies, Semantic Models & Knowledge Graphs](https://medium.com/@jim.mchugh/taxonomies-ontologies-semantic-models-knowledge-graphs-5aa4d4137eba)
- [Understanding Linked Data Formats](https://medium.com/wallscope/understanding-linked-data-formats-rdf-xml-vs-turtle-vs-n-triples-eb931dbe9827)
- [What Are Ontologies?](https://www.ontotext.com/knowledgehub/fundamentals/what-are-ontologies/?utm_source=chatgpt.com)
- [What Is the Semantic Web?](https://www.ontotext.com/knowledgehub/fundamentals/what-is-the-semantic-web/)
- [XML RDF](https://www.w3schools.com/xml/xml_rdf.asp)
