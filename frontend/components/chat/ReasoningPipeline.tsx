"use client";

import React, { useState } from "react";
import {
  ChevronDown,
  ChevronUp,
  AlertCircle,
  CheckCircle,
  Zap,
  RefreshCw,
  Image as ImageIcon,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface Stage {
  name: string;
  status: "pending" | "loading" | "complete" | "error";
  title: string;
  subtitle?: string;
  content?: any;
  concernCount?: number;
  changeCount?: number;
}

interface ReasoningPipelineProps {
  stages: Stage[];
  finalBuild?: any;
}

export function ReasoningPipeline({
  stages,
  finalBuild,
}: ReasoningPipelineProps) {
  const [expandedStage, setExpandedStage] = useState<number | null>(0);

  const getStageIcon = (status: string) => {
    switch (status) {
      case "loading":
        return <Zap className="w-5 h-5 animate-spin text-amber-500" />;
      case "complete":
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case "error":
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      default:
        return <div className="w-5 h-5 rounded-full border-2 border-gray-300" />;
    }
  };

  const getStageColor = (status: string) => {
    switch (status) {
      case "complete":
        return "border-l-4 border-green-500 bg-green-50";
      case "loading":
        return "border-l-4 border-amber-500 bg-amber-50";
      case "error":
        return "border-l-4 border-red-500 bg-red-50";
      default:
        return "border-l-4 border-gray-300 bg-gray-50";
    }
  };

  return (
    <div className="w-full space-y-3">
      {/* Pipeline Stages */}
      {stages.map((stage, idx) => (
        <motion.div
          key={idx}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: idx * 0.1 }}
        >
          <div
            className={`rounded-lg overflow-hidden cursor-pointer hover:shadow-md transition-shadow ${getStageColor(
              stage.status
            )}`}
            onClick={() =>
              setExpandedStage(expandedStage === idx ? null : idx)
            }
          >
            {/* Stage Header */}
            <div className="flex items-center justify-between p-4">
              <div className="flex items-center gap-3 flex-1">
                {getStageIcon(stage.status)}
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900">
                    Stage {idx + 1}: {stage.name}
                  </h3>
                  <p className="text-sm text-gray-600">{stage.subtitle}</p>
                </div>
              </div>

              {/* Metadata Badges */}
              <div className="flex items-center gap-3">
                {stage.concernCount !== undefined && (
                  <span className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded">
                    {stage.concernCount} concerns
                  </span>
                )}
                {stage.changeCount !== undefined && (
                  <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                    {stage.changeCount} changes
                  </span>
                )}

                {expandedStage === idx ? (
                  <ChevronUp className="w-5 h-5 text-gray-600" />
                ) : (
                  <ChevronDown className="w-5 h-5 text-gray-600" />
                )}
              </div>
            </div>

            {/* Stage Content (Expandable) */}
            <AnimatePresence>
              {expandedStage === idx && stage.content && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.3 }}
                  className="border-t border-gray-200 bg-white"
                >
                  <div className="p-4 text-sm">
                    {/* Build Stage Content */}
                    {stage.name === "Build" && (
                      <div className="space-y-3">
                        <div>
                          <h4 className="font-semibold text-gray-900 mb-2">
                            Initial Build
                          </h4>
                          {stage.content.build?.parts?.slice(0, 5).map(
                            (part: any, i: number) => (
                              <div
                                key={i}
                                className="flex justify-between items-start py-1"
                              >
                                <span className="text-gray-700">
                                  <span className="font-medium">
                                    {part.category}:
                                  </span>{" "}
                                  {part.name}
                                </span>
                                <span className="text-gray-900 font-semibold">
                                  ${part.price}
                                </span>
                              </div>
                            )
                          )}
                          <div className="flex justify-between items-center mt-2 pt-2 border-t border-gray-200">
                            <span className="font-semibold text-gray-900">
                              Total
                            </span>
                            <span className="font-bold text-lg text-gray-900">
                              ${stage.content.build?.total_budget}
                            </span>
                          </div>
                        </div>

                        {stage.content.reasoning?.tool_decisions && (
                          <div>
                            <h4 className="font-semibold text-gray-900 mb-2">
                              Tools Used
                            </h4>
                            {stage.content.reasoning.tool_decisions.map(
                              (tool: any, i: number) => (
                                <div
                                  key={i}
                                  className="bg-blue-50 p-2 rounded mb-1"
                                >
                                  <span className="font-medium text-blue-900">
                                    {tool.tool}
                                  </span>
                                  : {tool.why}
                                </div>
                              )
                            )}
                          </div>
                        )}
                      </div>
                    )}

                    {/* Critique Stage Content */}
                    {stage.name === "Critique" && (
                      <div className="space-y-3">
                        <div>
                          <p className="text-gray-700 mb-3">
                            <strong>Assessment:</strong>{" "}
                            {stage.content.critique?.overall_assessment}
                          </p>
                          <h4 className="font-semibold text-gray-900 mb-2">
                            Issues Found
                          </h4>
                        </div>

                        {stage.content.critique?.concerns?.slice(0, 3).map(
                          (concern: any, i: number) => (
                            <div
                              key={i}
                              className="bg-red-50 border border-red-200 p-3 rounded"
                            >
                              <div className="flex items-start gap-2">
                                <AlertCircle className="w-4 h-4 text-red-600 mt-0.5 flex-shrink-0" />
                                <div className="flex-1">
                                  <h5 className="font-semibold text-red-900">
                                    {concern.category}
                                  </h5>
                                  <p className="text-red-800 text-xs mt-1">
                                    {concern.issue}
                                  </p>
                                  {concern.evidence && (
                                    <p className="text-red-700 text-xs mt-1 italic">
                                      Evidence: {concern.evidence}
                                    </p>
                                  )}
                                </div>
                              </div>
                            </div>
                          )
                        )}
                      </div>
                    )}

                    {/* Improve Stage Content */}
                    {stage.name === "Improve" && (
                      <div className="space-y-3">
                        <div>
                          <h4 className="font-semibold text-gray-900 mb-2">
                            Changes Made
                          </h4>
                        </div>

                        {stage.content.revisions?.changes_made?.map(
                          (change: any, i: number) => (
                            <div
                              key={i}
                              className="bg-green-50 border border-green-200 p-3 rounded"
                            >
                              <div className="flex items-center gap-2">
                                <RefreshCw className="w-4 h-4 text-green-600 flex-shrink-0" />
                                <div className="flex-1">
                                  <p className="text-sm text-gray-800">
                                    <span className="font-medium line-through text-gray-600">
                                      {change.original_part}
                                    </span>
                                    <span className="mx-2">→</span>
                                    <span className="font-medium text-green-700">
                                      {change.revised_part}
                                    </span>
                                  </p>
                                  <p className="text-xs text-gray-600 mt-1">
                                    {change.reason}
                                  </p>
                                </div>
                              </div>
                            </div>
                          )
                        )}

                        {stage.content.revisions?.revised_build && (
                          <div className="bg-blue-50 p-3 rounded mt-3">
                            <p className="text-sm font-semibold text-blue-900 mb-2">
                              Revised Total Budget
                            </p>
                            <p className="text-2xl font-bold text-blue-900">
                              ${stage.content.revisions.revised_build.total_budget}
                            </p>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>
      ))}

      {/* Visualization Stage Content (New) */}
      {stages.map((stage, idx) => {
        if (stage.name !== "Visualization") return null;
        return (
          <AnimatePresence key={`viz-${idx}`}>
            {expandedStage === idx && stage.content && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: "auto", opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.3 }}
                className="border-t border-gray-200 bg-white"
              >
                <div className="p-4 text-sm">
                  <div className="space-y-3">
                    <div className="relative group rounded-xl overflow-hidden shadow-lg border border-gray-200">
                      {stage.content.image_url ? (
                        <img
                          src={stage.content.image_url}
                          alt="Generated PC Build"
                          className="w-full h-auto object-cover transform transition-transform hover:scale-105 duration-700"
                        />
                      ) : (
                        <div className="w-full h-64 bg-gray-100 flex items-center justify-center text-gray-400">
                          <Zap className="w-8 h-8 animate-pulse" />
                        </div>
                      )}
                      <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
                        <p className="text-white font-medium text-sm">AI Generated Visualization</p>
                        <p className="text-white/70 text-xs">{stage.content.source || "Vertex AI"}</p>
                      </div>
                    </div>
                    <p className="text-xs text-gray-500 italic border-l-2 border-gray-300 pl-2">
                      "{stage.content.prompt}"
                    </p>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        );
      })}

      {/* Final Build Summary */}
      {finalBuild && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: stages.length * 0.1 + 0.1 }}
          className="bg-gradient-to-r from-purple-50 to-blue-50 border-2 border-purple-200 rounded-lg p-4 mt-4"
        >
          <h3 className="font-bold text-lg text-gray-900 mb-3">Final Build</h3>
          <div className="space-y-2">
            {finalBuild.parts?.slice(0, 6).map((part: any, idx: number) => (
              <div
                key={idx}
                className="flex justify-between items-center py-2 border-b border-purple-100 last:border-b-0"
              >
                <div>
                  <span className="text-xs font-semibold text-purple-600">
                    {part.category}
                  </span>
                  <p className="text-gray-900">{part.name}</p>
                </div>
                <span className="font-bold text-gray-900">${part.price}</span>
              </div>
            ))}
          </div>
          <div className="flex justify-between items-center mt-4 pt-4 border-t-2 border-purple-200">
            <span className="font-bold text-lg text-gray-900">Total Budget</span>
            <span className="font-bold text-2xl text-purple-600">
              ${finalBuild.total_budget}
            </span>
          </div>
        </motion.div>
      )}
    </div>
  );
}
