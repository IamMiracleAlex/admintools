import { useState, useEffect } from "react";
import axios from "../../axios";

export const useDashboardState = () => {
  const [state, setState] = useState({
    urlStats: [],
    annotationStats: [],
    annotators: [],
    topAnnotators: [],
    statsBreakdown: [],
    status: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const fetchStatsAndAnnotators = () => {
    setError(false);
    setLoading(true);

    axios
      .get("server/url_stats_view/")
      .then((res) => {
        res.data.annotation_stats.categories.reverse();
        res.data.annotation_stats.annotated_figures.reverse();

        setState((prev) => ({
          ...prev,
          urlStats: res.data.stats.slice(0, 7),
          annotators: res.data.users.slice(1, 16),
          topAnnotators: res.data.top_annotators,
          annotationStats: res.data.annotation_stats,
          statsBreakdown: res.data.stats_breakdown,
        }));
        setLoading(false);
      })
      .catch((error) => {
        setError(true);
        console.log(error);
        setLoading(false);
      });
  };

  const fetchStatus = () => {
    setError(false);
    setLoading(true);

    axios
      .get("server/get-status/")
      .then((res) => {
        const cleanedData = res.data.MetricDataResults.filter(
          (table) => table.data.length > 1
        );

        setState((prev) => ({
          ...prev,
          status: cleanedData,
        }));
        setLoading(false);
      })
      .catch((error) => {
        setError(true);
        console.log(error);
        setLoading(false);
      });
  };

  // Fetch UrlStats and Annotators on mount
  useEffect(() => {
    fetchStatsAndAnnotators();
    fetchStatus();
  }, []);

  return [{ state, loading, error }, fetchStatsAndAnnotators];
};
