export const secsToMins = (secs) => {
  const mins = parseInt(Math.floor(secs / 60));
  let seconds = Math.round((secs % 60));
  if (seconds < 10) {
    seconds = `0${seconds}`;
  }
  return `${mins}:${seconds}`;
};

export const clamp = ({ value, min=-Infinity, max=Infinity }) => {
    return Math.max(Math.min(max, value), min);
};

export const generateButtonClass = ({ type='primary', size='large' }) => {
    return `btn btn-${type} btn-${size}`;
};

// lol Javascript
export const mod = (x, y) => ((x % y) + y) % y;

export const fetch = async (url) => {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = () => {
      if (xhr.readyState == XMLHttpRequest.DONE) {
          if (xhr.status === 200) {
              resolve(xhr.responseText);
          } else {
              reject({
                  errorText: xhr.statusText
              });
          }
      }
    }
    xhr.open('GET', url, true);
    xhr.send(null);
  });
};

export const fetchJSON = async (url) => {
  return JSON.parse(await fetch(url));
};

export const Key = {
    UP: 38,
    DOWN: 40,
    LEFT: 37,
    RIGHT: 39,
    ENTER: 13,
    SPACE: 32,
    ESCAPE: 27
};

export const isEmpty = obj => {
    return Object.keys(obj).length === 0 && obj.constructor === Object;
};

// Convert label file to object
export const parseLabels = (text) => {
  const labels = {};
  for (let line of text.split('\n')) {
    // Skip empty lines
    if (line === '') { continue; }

    const [start, end, label ] = line.split('\t');
    const times = [parseFloat(start), parseFloat(end)];

    if (start && end && label) {
      if (labels[label]) {
        labels[label].push(times);
      } else {
        labels[label] = [times];
      }
    } else {
      throw new Error('Cannot parse text file.');
    }
  }

  // Cache a list of ordered keys
  const orderedKeys = Object.keys(labels);
  orderedKeys.sort();
  labels.orderedKeys = orderedKeys;

  return labels;
}
