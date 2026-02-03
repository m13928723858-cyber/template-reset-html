import React, { useState, useCallback } from 'react';
import { Sparkles, Download, AlertCircle } from 'lucide-react';
import SimpleForm from './components/SimpleForm';
import ProgressDisplay from './components/ProgressDisplay';
import ResultDisplay from './components/ResultDisplay';
import { uploadImageOnly, generatePage, getTaskStatus, TaskStatus } from './api';

type AppStage = 'form' | 'processing' | 'completed' | 'error';

function SimpleApp() {
  const [stage, setStage] = useState<AppStage>('form');
  const [taskId, setTaskId] = useState<string>('');
  const [taskStatus, setTaskStatus] = useState<TaskStatus | null>(null);
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (winnerName: string, productType: string, imageFile: File | null) => {
    try {
      setError('');
      setLoading(true);
      
      // 1. 上传图片（如果有）
      let imageUrl = '';
      if (imageFile) {
        const uploadResult = await uploadImageOnly(imageFile);
        imageUrl = uploadResult.image_url;
      }
      
      // 2. 开始生成
      const result = await generatePage({
        winner_name: winnerName,
        product_type: productType,
        user_image_url: imageUrl || undefined,
      });
      
      setTaskId(result.task_id);
      setStage('processing');
      
      // 3. 开始轮询状态
      pollTaskStatus(result.task_id);
    } catch (err: any) {
      setError(err.response?.data?.detail || '生成失败，请重试');
      setStage('error');
    } finally {
      setLoading(false);
    }
  };

  const pollTaskStatus = useCallback((id: string) => {
    const interval = setInterval(async () => {
      try {
        const status = await getTaskStatus(id);
        setTaskStatus(status);

        if (status.status === 'completed') {
          clearInterval(interval);
          setStage('completed');
        } else if (status.status === 'failed') {
          clearInterval(interval);
          setError(status.error || '处理失败');
          setStage('error');
        }
      } catch (err: any) {
        clearInterval(interval);
        setError('获取状态失败');
        setStage('error');
      }
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  const handleReset = () => {
    setStage('form');
    setTaskId('');
    setTaskStatus(null);
    setError('');
    setLoading(false);
  };

  return (
    <div className="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12 animate-fade-in">
          <div className="flex items-center justify-center mb-4">
            <Sparkles className="w-12 h-12 text-indigo-600 mr-3" />
            <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              AI 页面生成器
            </h1>
          </div>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            输入产品信息，AI 自动生成完整营销页面
          </p>
        </div>

        {/* Main Content */}
        <div className="card p-8 animate-slide-up">
          {stage === 'form' && (
            <SimpleForm onSubmit={handleSubmit} loading={loading} />
          )}

          {stage === 'processing' && taskStatus && (
            <ProgressDisplay status={taskStatus} />
          )}

          {stage === 'completed' && taskStatus && (
            <ResultDisplay 
              status={taskStatus}
              taskId={taskId}
              onReset={handleReset}
            />
          )}

          {stage === 'error' && (
            <div className="text-center py-12">
              <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
              <h3 className="text-2xl font-semibold text-slate-800 mb-2">生成失败</h3>
              <p className="text-slate-600 mb-6">{error}</p>
              <button onClick={handleReset} className="btn-primary">
                重新开始
              </button>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-slate-500 text-sm">
          <p>Powered by Gemini AI & React</p>
          <p className="mt-2">
          </p>
        </div>
      </div>
    </div>
  );
}

export default SimpleApp;
