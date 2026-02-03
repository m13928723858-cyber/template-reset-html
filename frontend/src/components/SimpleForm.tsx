import React, { useState } from 'react';
import { Sparkles, Upload, Loader2, CheckCircle, AlertCircle } from 'lucide-react';

interface SimpleFormProps {
  onSubmit: (winnerName: string, productType: string, imageFile: File | null) => void;
  loading: boolean;
}

export default function SimpleForm({ onSubmit, loading }: SimpleFormProps) {
  const [winnerName, setWinnerName] = useState('');
  const [productType, setProductType] = useState('');
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string>('');

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImageFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (winnerName && productType) {
      onSubmit(winnerName, productType, imageFile);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="text-center mb-8">
        <Sparkles className="w-16 h-16 text-indigo-600 mx-auto mb-4" />
        <h2 className="text-3xl font-bold text-slate-800 mb-2">
          AI 智能页面生成
        </h2>
        <p className="text-slate-600">
          只需输入产品信息，AI 自动生成完整营销页面
        </p>
      </div>

      {/* Winner 产品名称 */}
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-2">
          Winner 产品名称 <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          value={winnerName}
          onChange={(e) => setWinnerName(e.target.value)}
          placeholder="例如: Ororo Heated Vest"
          className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
          required
          disabled={loading}
        />
        <p className="mt-1 text-sm text-slate-500">
          输入您要推广的产品名称
        </p>
      </div>

      {/* 产品类型 */}
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-2">
          产品类型 <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          value={productType}
          onChange={(e) => setProductType(e.target.value)}
          placeholder="例如: heated vest"
          className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
          required
          disabled={loading}
        />
        <p className="mt-1 text-sm text-slate-500">
          输入产品类型，用于生成竞品和搜索图片
        </p>
      </div>

      {/* 产品图片（可选） */}
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-2">
          产品主图 <span className="text-slate-400">(可选)</span>
        </label>
        <div className="flex items-center space-x-4">
          <label className="flex-1 cursor-pointer">
            <div className="border-2 border-dashed border-slate-300 rounded-lg p-6 text-center hover:border-indigo-500 transition-all">
              {imagePreview ? (
                <div className="space-y-2">
                  <img 
                    src={imagePreview} 
                    alt="Preview" 
                    className="max-h-32 mx-auto rounded"
                  />
                  <p className="text-sm text-slate-600">{imageFile?.name}</p>
                </div>
              ) : (
                <div className="space-y-2">
                  <Upload className="w-8 h-8 text-slate-400 mx-auto" />
                  <p className="text-sm text-slate-600">点击上传产品图片</p>
                  <p className="text-xs text-slate-400">支持 JPG, PNG, WEBP</p>
                </div>
              )}
            </div>
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              className="hidden"
              disabled={loading}
            />
          </label>
        </div>
        <p className="mt-1 text-sm text-slate-500">
          上传产品主图，将在页面中重复使用（如不上传，AI 将自动爬取）
        </p>
      </div>

      {/* 提交按钮 */}
      <button
        type="submit"
        disabled={loading || !winnerName || !productType}
        className="w-full btn-primary py-4 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? (
          <span className="flex items-center justify-center">
            <Loader2 className="w-5 h-5 mr-2 animate-spin" />
            AI 正在生成中...
          </span>
        ) : (
          <span className="flex items-center justify-center">
            <Sparkles className="w-5 h-5 mr-2" />
            开始生成页面
          </span>
        )}
      </button>

      {/* 功能说明 */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-6">
        <h3 className="font-semibold text-blue-900 mb-2 flex items-center">
          <CheckCircle className="w-5 h-5 mr-2" />
          AI 将自动完成
        </h3>
        <ul className="space-y-1 text-sm text-blue-800">
          <li>✓ 生成 4 个真实竞品</li>
          <li>✓ 生成完整营销文案（46个标题、37个段落、17个列表）</li>
          <li>✓ 智能爬取 9 张产品图片</li>
          <li>✓ 自动填充到专业模板</li>
        </ul>
      </div>
    </form>
  );
}
