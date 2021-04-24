const composer = require('openwhisk-composer')

module.exports = composer.sequence(
    'resize',
    'mirror',
    'greyscale'
)
