from pathlib import Path

from pylexibank.dataset import MyDataset
from pylexibank.util import pb

# Customize your basic data
import attr
from pylexibank import Concept, Language, Lexeme, Cognate

@attr.s
class NewConcept(Concept):
    Attribute1 = attr.ib(default=None)
    Attribute2 = attr.ib(default=None)

@attr.s
class NewLanguage(Language):
    Attribute1 = attr.ib(default=None)
    Attribute2 = attr.ib(default=None)

@attr.s
class NewLexeme(Lexeme):
    Attribute1 = attr.ib(default=None)
    Attribute2 = attr.ib(default=None)

@attr.s
class NewCognate(Cognate):
    Attribute1 = attr.ib(default=None)
    Attribute2 = attr.ib(default=None)

# form specification
from pylexibank.forms import FormSpec

class Dataset(MyDataset):
    dir = Path(__file__).parent
    id = "template"

    # add your personalized data types here
    concept_class = MyConcept
    language_class = MyLanguage
    lexeme_class = MyLexeme
    cognate_class = MyCognate

    # define the way in which forms should be handled
    form_spec = FormSpec(
            brackets={"(": ")"},
            separators = ";/,",
            missing_data = ('?', '-'),
            strip_inside_brackets=True
            )

    def cmd_download(self, args):
        with self.raw_dir.temp_download(
                "http://www.example.com",
                "example.tsv"
                ) as p:
            data = p

        self.raw_dir.write_csv(
            'template.csv',
            [x for x in data]
            )

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.
        """
        data = self.raw_dir.read_csv('template.csv', dicts=True)
        languages, concepts = {}, {}
        
        # short cut to add concepts and languages, provided your name spaces
        # match
        args.writer.add_concepts()
        args.writer.add_languages()

        # detailed way to do it
        for concept in self.concepts:
            args.writer.add_concept(
                    ID=concept['ID'],
                    Name=concept['ENGLISH'])
                    Concepticon_ID=concept['CONCEPTICON_ID'],
        for language in self.languages:
            args.writer.add_language(
                    ID=language['ID'],
                    Glottolog=language['Glottolog']
                    )

        for concept in self.conceptlist.concepts.values():
            args.writer.add_concept(
                    ID=concept.number,
                    Name=concept.gloss,
                    Concepticon_ID=concept.concepticon_id,
                    Concepticon_Gloss=concept.concepticon_gloss,
                    Chinese_Gloss=concept.attributes['chinese']
            )
            concepts[concept.attributes['chinese']] = concept.number

        
        for row in pb(data, desc='cldfify'):
            # add form without segments
            lex = args.writer.add_form(
                    Language_ID=row['Language_ID'],
                    Parameter_ID=row['Parameter_ID'],
                    Value=row['Word'],
                    Form=row['Word'],
                    Source=[row['Source']],
                    )
            args.writer.add_cognate(
                    lexeme=lex,
                    Cognateset_ID=line['Cognateset_ID']
                    )

            # add form with segments
            lex = args.writer.add_form_with_segments(
                    Language_ID=row['Language_ID'],
                    Parameter_ID=row['Parameter_ID'],
                    Value=row['Word'],
                    Form=row['Word'],
                    Segments=row['Segments'],
                    Source=[row['Source']],
                    )
            args.writer.add_cognate(
                    lexeme=lex,
                    Cognateset_ID=line['Cognateset_ID']
                    )

            # add forms from value 
            for lex in args.writer.add_forms_from_value(
                    Language_ID=row['Language_ID'],
                    Parameter_ID=row['Parameter_ID'],
                    Value=row['Word'],
                    Source=[row['Source']],
                    ):
                args.writer.add_cognate(
                        lexeme=lex,
                        Cognateset_ID=line['Cognateset_ID']
                        )


                    
