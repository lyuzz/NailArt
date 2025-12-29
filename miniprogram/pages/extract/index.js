import { uploadFile } from '../../utils/upload';
import { pollJob } from '../../utils/poll';
import { request, makeUrl } from '../../utils/api';

Page({
  data: {
    previewUrl: '',
    nails: [],
    loading: false,
    suggestedAsset: null
  },
  chooseImage() {
    wx.chooseImage({
      count: 1,
      success: async (res) => {
        const filePath = res.tempFilePaths[0];
        this.setData({ loading: true });
        try {
          const job = await uploadFile({ filePath, url: '/v1/extract' });
          const result = await pollJob(job.job_id);
          const nails = result.output.nails.map((nail) => ({
            ...nail,
            rgba_url: makeUrl(nail.rgba_url),
            mask_url: makeUrl(nail.mask_url)
          }));
          const suggestedAsset = result.output.suggested_asset;
          this.setData({
            previewUrl: makeUrl(result.output.preview_url),
            nails,
            suggestedAsset,
            loading: false
          });
        } catch (err) {
          this.setData({ loading: false });
          wx.showToast({ title: '处理失败', icon: 'error' });
        }
      }
    });
  },
  async saveAsset() {
    const asset = this.data.suggestedAsset;
    if (!asset) return;
    try {
      await request({ url: '/v1/assets', method: 'POST', data: asset });
      wx.navigateTo({ url: '/pages/library/index' });
    } catch (err) {
      wx.showToast({ title: '保存失败', icon: 'error' });
    }
  }
});
