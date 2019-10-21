from pathlib import Path
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import pb
from pylexibank.forms import FormSpec

# Customize your basic data.
# if you need to store other data in columns than the lexibank defaults, then over-ride
# the table type and add the required columns e.g. 
#
# import attr
# from pylexibank import Concept as BaseConcept  ( or Language, Lexeme, or Cognate)
#
# @attr.s
# class Concept(Concept):
#    MyAttribute1 = attr.ib(default=None)

class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "template"  # TODO - update this to match your datasets's name!

    # add your personalized data types here (or language_class, lexeme_class, cognate_class)
    #concept_class = MyConcept

    # define the way in which forms should be handled
    form_spec = FormSpec(
        brackets = {"(": ")"},  # characters that function as brackets
        separators = ";/,",  # characters that split forms e.g. "a, b".
        missing_data = ('?', '-'),  # characters that denote missing data.
        strip_inside_brackets = True   # do you want data removed in brackets or not?
    )

    def cmd_download(self, args):
        with self.raw_dir.temp_download("http://www.example.com", "example.tsv") as data:
            self.raw_dir.write_csv('template.csv', data)

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.
        """
        data = self.raw_dir.read_csv('template.csv', dicts=True)
        
        # short cut to add concepts and languages, provided your name spaces
        # match lexibank's expected format.
        args.writer.add_concepts()
        args.writer.add_languages()

        # if not, then here is a more detailed way to do it:
        # for concept in self.concepts:
        #     args.writer.add_concept(
        #         ID=concept['ID'],
        #         Name=concept['ENGLISH'],
        #         Concepticon_ID=concept['CONCEPTICON_ID']
        #     )
        # for language in self.languages:
        #     args.writer.add_language(
        #         ID=language['ID'],
        #         Glottolog=language['Glottolog']
        #     )
        
        # add data
        for row in pb(data, desc='cldfify'):
            # .. if you have segmentable data, replace `add_form` with `add_form_with_segments`
            # .. TODO @Mattis, when should we use add_forms_from_value() instead?
            lex = args.writer.add_form(
                Language_ID=row['Language_ID'],
                Parameter_ID=row['Parameter_ID'],
                Value=row['Word'],
                Form=row['Word'],
                Source=[row['Source']],
            )
            
            # add cognates -- make sure Cognateset_ID is global! 
            args.writer.add_cognate(
                lexeme=lex,
                Cognateset_ID=line['Cognateset_ID']
            )
