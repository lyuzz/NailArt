import { BASE_URL } from '../env';

export function makeUrl(path) {
  if (!path) return '';
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path;
  }
  return `${BASE_URL}${path}`;
}

export function request({ url, method = 'GET', data }) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: makeUrl(url),
      method,
      data,
      success: (res) => resolve(res.data),
      fail: reject
    });
  });
}
