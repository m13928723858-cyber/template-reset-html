import React from 'react';
import { Loader2, CheckCircle, Image, FileText, Package } from 'lucide-react';
import { TaskStatus } from '../api';

interface ProgressDisplayProps {
  status: TaskStatus;
}

function ProgressDisplay({ status }: ProgressDisplayProps) {
  const { progress } = status;
  const percentage = progress.percentage || 0;

  const getStageIcon = (stage: string) => {
    switch (stage) {
      case 'extracting':
        return <Package className="w-6 h-6" />;
      case 'identifying_brands':
      case 'brands_identified':
        return <CheckCircle className="w-6 h-6" />;
      case 'crawling_images':
      case 'images_crawled':
        return <Image className="w-6 h-6" />;
      case 'replacing_content':
      case 'content_replaced':
        return <FileText className="w-6 h-6" />;
      case 'packaging':
        return <Package className="w-6 h-6" />;
      default:
        return <Loader2 className="w-6 h-6 animate-spin" />;
    }
  };

  const getStageTitle = (stage: string) => {
    const titles: Record<string, string> = {
      initializing: '初始化中...',
      extracting: '解压文件中...',
      identifying_brands: '识别品牌中...',
      brands_identified: '品牌识别完成',
      crawling_images: '爬取图片中...',
      images_crawled: '图片爬取完成',
      replacing_content: '替换内容中...',
      content_replaced: '内容替换完成',
      packaging: '打包文件中...',
      completed: '处理完成！',
    };
    return titles[stage] || '处理中...';
  };

  return (
    <div className="py-8">
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full mb-4 animate-pulse-slow">
          {getStageIcon(progress.stage)}
        </div>
        <h2 className="text-2xl font-bold text-slate-800 mb-2">
          {getStageTitle(progress.stage)}
        </h2>
        <p className="text-slate-600">{progress.message}</p>
      </div>

      {/* Progress Bar */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-semibold text-slate-700">处理进度</span>
          <span className="text-sm font-bold text-blue-600">{percentage}%</span>
        </div>
        <div className="h-3 bg-slate-200 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-blue-600 to-indigo-600 transition-all duration-500 ease-out"
            style={{ width: `${percentage}%` }}
          />
        </div>
      </div>

      {/* Brands Display */}
      {progress.brands && progress.brands.length > 0 && (
        <div className="mb-6 p-6 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl">
          <h3 className="font-semibold text-slate-800 mb-3 flex items-center">
            <CheckCircle className="w-5 h-5 text-green-500 mr-2" />
            已识别品牌
          </h3>
          <div className="flex flex-wrap gap-2">
            {progress.brands.map((brand, index) => (
              <span
                key={index}
                className="px-4 py-2 bg-white border-2 border-blue-300 rounded-lg font-semibold text-blue-700 shadow-sm"
              >
                {brand}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Images Count */}
      {progress.images_count && progress.images_count > 0 && (
        <div className="mb-6 p-6 bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-xl">
          <h3 className="font-semibold text-slate-800 mb-2 flex items-center">
            <Image className="w-5 h-5 text-green-500 mr-2" />
            图片爬取统计
          </h3>
          <p className="text-2xl font-bold text-green-700">
            {progress.images_count} 张图片
          </p>
        </div>
      )}

      {/* Processing Steps */}
      <div className="space-y-3">
        <ProcessStep
          title="解压和分析"
          completed={percentage > 10}
          active={percentage <= 10}
        />
        <ProcessStep
          title="识别品牌"
          completed={percentage > 30}
          active={percentage > 10 && percentage <= 30}
        />
        <ProcessStep
          title="爬取图片"
          completed={percentage > 60}
          active={percentage > 30 && percentage <= 60}
        />
        <ProcessStep
          title="替换内容"
          completed={percentage > 85}
          active={percentage > 60 && percentage <= 85}
        />
        <ProcessStep
          title="打包输出"
          completed={percentage >= 100}
          active={percentage > 85 && percentage < 100}
        />
      </div>

      <div className="mt-8 text-center text-sm text-slate-500">
        <p>处理时间取决于网页大小和图片数量，请耐心等待...</p>
      </div>
    </div>
  );
}

interface ProcessStepProps {
  title: string;
  completed: boolean;
  active: boolean;
}

function ProcessStep({ title, completed, active }: ProcessStepProps) {
  return (
    <div className="flex items-center">
      <div
        className={`w-8 h-8 rounded-full flex items-center justify-center transition-all duration-300 ${
          completed
            ? 'bg-green-500 text-white'
            : active
            ? 'bg-blue-500 text-white animate-pulse'
            : 'bg-slate-200 text-slate-400'
        }`}
      >
        {completed ? (
          <CheckCircle className="w-5 h-5" />
        ) : active ? (
          <Loader2 className="w-5 h-5 animate-spin" />
        ) : (
          <div className="w-2 h-2 bg-slate-400 rounded-full" />
        )}
      </div>
      <span
        className={`ml-3 font-medium ${
          completed || active ? 'text-slate-800' : 'text-slate-400'
        }`}
      >
        {title}
      </span>
    </div>
  );
}

export default ProgressDisplay;
