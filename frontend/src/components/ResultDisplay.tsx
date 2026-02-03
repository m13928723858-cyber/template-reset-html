import React from 'react';
import { Download, CheckCircle, Image, FileText, RotateCcw, TrendingUp } from 'lucide-react';
import { TaskStatus, downloadResult } from '../api';

interface ResultDisplayProps {
  status: TaskStatus;
  taskId: string;
  onReset: () => void;
}

function ResultDisplay({ status, taskId, onReset }: ResultDisplayProps) {
  const report = status.report;

  const handleDownload = () => {
    window.open(downloadResult(taskId), '_blank');
  };

  return (
    <div className="py-8">
      {/* Success Header */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-green-500 to-emerald-600 rounded-full mb-4 animate-bounce">
          <CheckCircle className="w-12 h-12 text-white" />
        </div>
        <h2 className="text-3xl font-bold text-slate-800 mb-2">
          处理完成！
        </h2>
        <p className="text-slate-600">您的网页已成功改造</p>
      </div>

      {/* Statistics */}
      {report && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
          <div className="p-6 bg-gradient-to-br from-blue-50 to-blue-100 border border-blue-200 rounded-xl">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-blue-700 font-medium mb-1">图片替换</p>
                <p className="text-3xl font-bold text-blue-900">{report.images_replaced}</p>
              </div>
              <Image className="w-12 h-12 text-blue-500 opacity-50" />
            </div>
          </div>

          <div className="p-6 bg-gradient-to-br from-purple-50 to-purple-100 border border-purple-200 rounded-xl">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-purple-700 font-medium mb-1">文案替换</p>
                <p className="text-3xl font-bold text-purple-900">{report.texts_replaced}</p>
              </div>
              <FileText className="w-12 h-12 text-purple-500 opacity-50" />
            </div>
          </div>
        </div>
      )}

      {/* Brands Used */}
      {report && Object.keys(report.brands_used).length > 0 && (
        <div className="mb-8 p-6 bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-200 rounded-xl">
          <h3 className="font-semibold text-slate-800 mb-4 flex items-center">
            <TrendingUp className="w-5 h-5 text-indigo-600 mr-2" />
            品牌使用统计
          </h3>
          <div className="space-y-3">
            {Object.entries(report.brands_used).map(([brand, count]) => {
              const total = Object.values(report.brands_used).reduce((a, b) => a + b, 0);
              const percentage = Math.round((count / total) * 100);
              
              return (
                <div key={brand}>
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-semibold text-slate-700">{brand}</span>
                    <span className="text-sm text-slate-600">{count} 张 ({percentage}%)</span>
                  </div>
                  <div className="h-2 bg-slate-200 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-indigo-500 to-purple-500"
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Errors */}
      {report && report.errors && report.errors.length > 0 && (
        <div className="mb-8 p-6 bg-yellow-50 border border-yellow-200 rounded-xl">
          <h3 className="font-semibold text-yellow-900 mb-3">
            ⚠️ 处理警告
          </h3>
          <ul className="space-y-1 text-sm text-yellow-800">
            {report.errors.slice(0, 5).map((error, index) => (
              <li key={index}>• {error}</li>
            ))}
            {report.errors.length > 5 && (
              <li className="text-yellow-600">... 还有 {report.errors.length - 5} 个警告</li>
            )}
          </ul>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex gap-4">
        <button
          onClick={handleDownload}
          className="btn-primary flex-1 flex items-center justify-center"
        >
          <Download className="w-5 h-5 mr-2" />
          下载改造后的网页
        </button>
        <button
          onClick={onReset}
          className="btn-secondary flex items-center"
        >
          <RotateCcw className="w-5 h-5 mr-2" />
          处理新文件
        </button>
      </div>

      {/* Info Box */}
      <div className="mt-8 p-6 bg-slate-50 border border-slate-200 rounded-xl">
        <h3 className="font-semibold text-slate-800 mb-3">📦 下载说明</h3>
        <ul className="space-y-2 text-sm text-slate-600">
          <li>• 下载的 ZIP 文件包含完整的改造后网页</li>
          <li>• 解压后可直接在浏览器中打开 HTML 文件查看效果</li>
          <li>• 包含详细的替换报告（REPLACEMENT_REPORT.json）</li>
          <li>• 所有图片和文案已自动替换完成</li>
        </ul>
      </div>
    </div>
  );
}

export default ResultDisplay;
