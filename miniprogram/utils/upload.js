import { BASE_URL } from '../env';

export function uploadFile({ filePath, url, formData = {} }) {
  return new Promise((resolve, reject) => {
    wx.uploadFile({
      url: `${BASE_URL}${url}`,
      filePath,
      name: 'file',
      formData,
      success: (res) => {
        try {
          const data = JSON.parse(res.data);
          resolve(data);
        } catch (err) {
          reject(err);
        }
      },
      fail: reject
    });
  });
}
