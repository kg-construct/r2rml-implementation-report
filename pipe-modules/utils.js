function processAssertions(data) {
  if (data.data.length > 0 && data.data[0].assertions) {
    const testCases = data.data;

    testCases.forEach(testCase => {
      const newAssertions = {};

      testCase.assertions.forEach(assertion => {
        newAssertions[assertion.processor] = assertion.result.outcome;
      });

      testCase.assertions = newAssertions;
    });
  }

  return data;
}

function formatDate(data) {
  if (data.data.length > 0 && data.data[0].version) {
    data.data.forEach(processor => {
      const date = new Date(processor.date);
      const day = ('' + date.getDate()).padStart(2, '0');
      const month = ('' + (date.getMonth() + 1)).padStart(2, '0');

      processor.date = date.getFullYear() + '-' + month + '-' + day;
    });
  }

  return data;
}

function setRDBMS(data) {
  if (data.data.length > 0 && data.data[0].version) {
    data.data.forEach(processor => {
      const matches = processor.name.match(/-([^-]+)$/);
      processor.rdbms = matches[1].toLowerCase();
      processor.name = processor.name.replace(matches[0], '');
    });

    console.log(data);
  }

  return data;
}

module.exports = {
  processAssertions,
  formatDate,
  setRDBMS
}
