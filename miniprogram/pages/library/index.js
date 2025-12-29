import { request, makeUrl } from '../../utils/api';

Page({
  data: {
    assets: []
  },
  onShow() {
    this.fetchAssets();
  },
  async fetchAssets() {
    const data = await request({ url: '/v1/assets?owner_type=all' });
    const assets = data.map((asset) => ({
      ...asset,
      preview_url: makeUrl(asset.preview_url)
    }));
    this.setData({ assets });
  },
  goTryon(e) {
    const assetId = e.currentTarget.dataset.id;
    wx.navigateTo({ url: `/pages/tryon/index?asset_id=${assetId}` });
  }
});
