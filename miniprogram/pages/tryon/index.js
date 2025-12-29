import { uploadFile } from '../../utils/upload';
import { pollJob } from '../../utils/poll';
import { makeUrl } from '../../utils/api';

Page({
  data: {
    assetId: '',
    resultUrl: '',
    debugUrl: '',
    loading: false
  },
  onLoad(query) {
    this.setData({ assetId: query.asset_id || '' });
  },
  chooseImage() {
    const { assetId } = this.data;
    if (!assetId) {
      wx.showToast({ title: '缺少素材', icon: 'error' });
      return;
    }
    wx.chooseImage({
      count: 1,
      success: async (res) => {
        const filePath = res.tempFilePaths[0];
        this.setData({ loading: true });
        try {
          const job = await uploadFile({
            filePath,
            url: '/v1/tryon',
            formData: { asset_id: assetId }
          });
          const result = await pollJob(job.job_id);
          this.setData({
            resultUrl: makeUrl(result.output.result_url),
            debugUrl: makeUrl(result.output.debug_url),
            loading: false
          });
        } catch (err) {
          this.setData({ loading: false });
          wx.showToast({ title: '处理失败', icon: 'error' });
        }
      }
    });
  },
  saveImage() {
    const { resultUrl } = this.data;
    if (!resultUrl) return;
    wx.downloadFile({
      url: resultUrl,
      success: (res) => {
        wx.saveImageToPhotosAlbum({
          filePath: res.tempFilePath,
          success: () => wx.showToast({ title: '已保存' }),
          fail: () => wx.showToast({ title: '保存失败', icon: 'error' })
        });
      },
      fail: () => wx.showToast({ title: '下载失败', icon: 'error' })
    });
  }
});
