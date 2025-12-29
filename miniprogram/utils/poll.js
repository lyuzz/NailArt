import { request } from './api';

export function pollJob(jobId, interval = 1500, timeout = 60000) {
  const start = Date.now();
  return new Promise((resolve, reject) => {
    const tick = () => {
      request({ url: `/v1/jobs/${jobId}` })
        .then((data) => {
          if (data.status === 'done') {
            resolve(data);
            return;
          }
          if (data.status === 'failed') {
            reject(data.error || { message: 'failed' });
            return;
          }
          if (Date.now() - start > timeout) {
            reject({ message: 'timeout' });
            return;
          }
          setTimeout(tick, interval);
        })
        .catch(reject);
    };
    tick();
  });
}
