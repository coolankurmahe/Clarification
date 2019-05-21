from collections import defaultdict
from logging import getLogger

import flask_restful
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)
api = flask_restful.Api(app)

_logger = getLogger(__name__)


def _build_histogram(file_name='/home/oren/work/walmartca/hackathon/query_count_concept_attributes.tsv'):
    print 'Loading'
    _logger.info('Building histogram')
    df = pd.read_csv(file_name, sep='\t')

    histogram = (pd.DataFrame({
                                  "count": row['counts'],
                                  "concept": row.concepts,
                                  "attribute": attribute
                              }
                              for i, row in df.iterrows() for attribute in
                              str(row.paths).replace('-', '').split(',')
                              )
                 .groupby(['concept', 'attribute'])['count'].sum()
                 )

    concept_attribute_count = defaultdict(dict)

    for record in histogram.reset_index().to_dict(orient='records'):
        if not record['attribute']:
            continue
        concept_attribute_count[record['concept']][record['attribute']] = record['count']
    concept_attribute_count = dict(concept_attribute_count)
    _logger.info('Building histogram DONE')
    return concept_attribute_count


histogram = _build_histogram()


@app.route('/get_popular_attributes')
def get():
    return jsonify(_get_attributes(request.args['concept']))


def _get_attributes(concept):
    _logger.info('Get attributes for concept %s', concept)
    attributes = histogram[concept]
    return sorted(attributes.keys(), key=lambda attr: attributes[attr], reverse=True)


app.run(debug=True)

